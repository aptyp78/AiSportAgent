// app/page.tsx
import Image from "next/image";

export const metadata = {
  title: "AI-Sport Agent",
  description: "Интеллектуальный ассистент для спорта на базе LLM",
};

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 space-y-8 bg-gray-50">
      <h1 className="text-4xl font-bold text-gray-900">
        Добро пожаловать в <span className="text-indigo-600">AI-Sport Agent</span>
      </h1>

      <p className="max-w-xl text-center text-gray-600">
        Платформа, которая превращает данные о тренировках в персональные рекомендации
        с помощью больших языковых моделей.
      </p>

      <Image
        src="/logo.png"            // положите логотип в /public/logo.png
        alt="AI-Sport Agent logo"
        width={160}
        height={160}
        priority
      />
    </main>
  );
}
