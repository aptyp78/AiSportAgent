// app/layout.tsx
// import "./globals.css";

export const metadata = { title: "AI-Sport Agent" };

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  );
}
/* No additional code needed here. The RootLayout component is correctly implemented for a Next.js app layout file. */