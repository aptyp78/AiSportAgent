import os
from fitparse import FitFile

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../../Data')
FILES = [
    "RunGarminNoPower.fit",
    "RunGarminStrydPower.fit",
    "RunStryd.fit"
]

FIELDS = {
    "GPS (latitude, longitude)": ("position_lat", "position_long"),
    "Power": ("power",),
    "Heart Rate": ("heart_rate",),
    "Cadence": ("cadence",),
    "Altitude": ("altitude",),
    "Pace": ("speed",),  # pace = 1/speed, если есть speed
    "Ground Contact Time": ("ground_contact_time",),
    "Vertical Oscillation": ("vertical_oscillation",)
}

def check_fields_in_fit(filepath):
    fitfile = FitFile(filepath)
    present = {key: False for key in FIELDS}
    for record in fitfile.get_messages("record"):
        for field_name, fit_keys in FIELDS.items():
            for key in fit_keys:
                if record.get_value(key) is not None:
                    present[field_name] = True
    return present

def main():
    results = {}
    for fname in FILES:
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            print(f"Файл не найден: {path}")
            continue
        results[fname] = check_fields_in_fit(path)

    # Формируем отчёт
    print("Сравнение наличия данных в FIT-файлах:\n")
    header = ["Данные"] + FILES
    print("{:<30} {:<22} {:<22} {:<22}".format(*header))
    print("-" * 100)
    for field in FIELDS:
        row = [field]
        for fname in FILES:
            val = results.get(fname, {}).get(field, False)
            row.append("Есть" if val else "Нет")
        print("{:<30} {:<22} {:<22} {:<22}".format(*row))

if __name__ == "__main__":
    main()
