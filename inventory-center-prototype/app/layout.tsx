import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ERP 库存中心原型",
  description: "跨境电商卖家 ERP 库存中心管理设计原型"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
