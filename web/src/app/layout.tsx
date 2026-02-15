import type { Metadata } from "next";
import { Inter, JetBrains_Mono, Noto_Sans_Gujarati } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });
const notoSansGujarati = Noto_Sans_Gujarati({ subsets: ["gujarati"], variable: "--font-gujarati" });

export const metadata: Metadata = {
  title: "Gujarati Python - Program in Your Language",
  description: "The world's first complete Python programming environment in the Gujarati language.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="gu">
      <body className={cn(
        inter.variable,
        jetbrainsMono.variable,
        notoSansGujarati.variable,
        "min-h-screen bg-white font-sans text-slate-950 antialiased dark:bg-slate-950 dark:text-slate-50 selection:bg-blue-500 selection:text-white"
      )}>
        {/* Grid Background Overlay */}
        <div className="fixed inset-0 z-[-1] pointer-events-none bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

        {children}
      </body>
    </html>
  );
}
