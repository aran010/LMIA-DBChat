import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Offline AI Knowledge Assistant",
  description: "Secure, offline AI powered by your company data.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
