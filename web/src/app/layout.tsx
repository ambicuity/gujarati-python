import type { Metadata } from "next";
import { Inter, JetBrains_Mono, Noto_Sans_Gujarati } from "next/font/google";
import "./globals.css";
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });
const notoSansGujarati = Noto_Sans_Gujarati({ subsets: ["gujarati"], variable: "--font-gujarati" });

export const metadata: Metadata = {
  title: "Gujarati Python - Program in Your Mother Tongue",
  description: "The world's first complete Python programming environment in the Gujarati language. Write code, build apps, and learn programming in Gujarati.",
  keywords: ["Gujarati Python", "Python in Gujarati", "Gujarati Programming", "Learn Python Gujarati", "Coding in Mother Tongue", "India Coding", "Regional Language Programming", "Python wrapper"],
  authors: [{ name: "Ritesh Rana", url: "https://riteshrana.engineer" }],
  creator: "Ritesh Rana",
  metadataBase: new URL("https://ambicuity.github.io/gujarati-python/"),
  openGraph: {
    type: "website",
    locale: "gu_IN",
    url: "https://ambicuity.github.io/gujarati-python/",
    title: "Gujarati Python - Program in Your Mother Tongue",
    description: "Break the language barrier. Build powerful software using the syntax you dream in. A complete Python implementation for Gujarati speakers.",
    siteName: "Gujarati Python",
    images: [
      {
        url: "/og-image.png", // We should create this or use a placeholder
        width: 1200,
        height: 630,
        alt: "Gujarati Python Hero"
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title: "Gujarati Python - Program in Your Mother Tongue",
    description: "The world's first complete Python programming environment in the Gujarati language.",
    creator: "@riteshrana", // Assuming or placeholder
    images: ["/og-image.png"]
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="gu" suppressHydrationWarning>
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
