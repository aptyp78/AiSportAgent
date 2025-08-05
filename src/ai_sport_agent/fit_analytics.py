#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

from ai_sport_agent.db import init_db, get_conn
from ai_sport_agent.parser import parse_fit

def cmd_ingest(args):
    """
    Импортирует все .fit-файлы из указанных путей в базу,
    очищая старые интервалы для тех же файлов.
    """
    init_db()
    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(path.rglob("*.fit"))
        elif path.suffix.lower() == ".fit":
            files.append(path)
    if not files:
        print("⚠️  Не найдено ни одного .fit-файла в указанных путях.", file=sys.stderr)
        return

    conn = get_conn()
    cur = conn.cursor()
    # Удаляем старые интервалы для этих файлов
    for f in files:
        cur.execute(
            "DELETE FROM intervals WHERE session_id IN (SELECT id FROM sessions WHERE file=?)",
            (str(f),)
        )
    conn.commit()

    count = 0
    for f in files:
        print(f"Парсим {f}…")
        session = parse_fit(f)

        # Сохраняем сессию
        cur.execute(
            "INSERT OR IGNORE INTO sessions(file, date, mode) VALUES (?, ?, ?)",
            (session["file"], session["date"], session["mode"])
        )
        conn.commit()

        # Получаем её ID
        cur.execute("SELECT id FROM sessions WHERE file = ?", (session["file"],))
        session_id = cur.fetchone()["id"]

        # Сохраняем интервалы
        for iv in session["intervals"]:
            cur.execute(
                """
                INSERT INTO intervals(session_id, type, start, end, duration, avg_power)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    iv.get("type"),
                    iv.get("start"),
                    iv.get("end"),
                    iv.get("duration"),
                    iv.get("avg_power"),
                )
            )
        conn.commit()
        count += 1

    print(f"✅ Импортировано {count} файлов.")

def cmd_summarize(args):
    """
    Выводит статистику по интервалам:
      • sessions_count — число сессий
      • total_duration — суммарная длительность в секундах
    По флагу --week берёт последние 7 дней (включительно),
    иначе по --start/--end.
    """
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    if args.week:
        today = datetime.now().date()
        start = (today - timedelta(days=7)).isoformat()
        end = today.isoformat()
    else:
        start = args.start or (datetime.now().date() - timedelta(days=7)).isoformat()
        end = args.end or datetime.now().date().isoformat()

    print(f"Сводка с {start} по {end}")
    cur.execute(
        """
        SELECT 
          COUNT(DISTINCT session_id) AS sessions_count,
          SUM(duration)            AS total_duration
        FROM intervals
        WHERE date(start) BETWEEN ? AND ?
        """,
        (start, end)
    )
    res = cur.fetchone()
    print(f"Сессий: {res['sessions_count']}, общий объём (сек): {res['total_duration']}")

def cmd_classify_races(args):
    """
    Классифицирует будущие старты (A–C).
    Пока не реализовано.
    """
    print("Классификация стартов пока не реализована.")

def cmd_plan(args):
    """
    Генерирует недельный план 80/20.
    Пока не реализовано.
    """
    print("Генерация плана пока не реализована.")

def main():
    parser = argparse.ArgumentParser(prog="fit-analytics")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("ingest", help="Импорт .fit-файлов в базу")
    p.add_argument("paths", nargs="+", help=".fit files or directories")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("summarize", help="Сводка по тренировкам")
    p.add_argument("--week", action="store_true", help="Последние 7 дней")
    p.add_argument("--start", help="Дата начала YYYY-MM-DD")
    p.add_argument("--end", help="Дата окончания YYYY-MM-DD")
    p.set_defaults(func=cmd_summarize)

    p = sub.add_parser("classify-races", help="Классификация стартов A–C")
    p.set_defaults(func=cmd_classify_races)

    p = sub.add_parser("plan", help="Генерация недельного плана")
    p.add_argument("--week", action="store_true", help="План на неделю")
    p.set_defaults(func=cmd_plan)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
