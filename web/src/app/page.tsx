"use client";

import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import Link from "next/link";
import { Check, Copy, Terminal, Code2, Globe, Sparkles, X } from "lucide-react";
import { useState } from "react";

import { HeroCodeCard } from "../components/ui/hero-code-card";
import { AnimatePresence } from "framer-motion";

export default function Home() {
  const [copied, setCopied] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const copyCommand = () => {
    navigator.clipboard.writeText("pip install gujarati-python");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const navLinks = [
    { name: "FEATURES", href: "#features" },
    { name: "INSTALL", href: "#install" },
    { name: "DOCS", href: "/docs" },
    { name: "GITHUB", href: "https://github.com/ambicuity/gujarati-python" },
  ];

  return (
    <main className="flex min-h-screen flex-col items-center justify-between pb-24">
      {/* Navbar */}
      <nav className="w-full border-b border-black/5 dark:border-white/5 bg-white/50 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="font-mono text-sm tracking-widest text-blue-600 font-bold z-50 relative">GUJARATI_PYTHON_V1.0</div>

          {/* Desktop Nav */}
          <div className="hidden md:flex gap-6 text-sm font-medium text-slate-500">
            {navLinks.map(link => (
              <a key={link.name} href={link.href} className="hover:text-blue-600 transition-colors">{link.name}</a>
            ))}
          </div>

          {/* Mobile Nav Button */}
          <button
            className="md:hidden z-50 p-2 text-slate-600"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <div className="space-y-1.5">
              <span className="block w-6 h-0.5 bg-current"></span>
              <span className="block w-6 h-0.5 bg-current"></span>
              <span className="block w-6 h-0.5 bg-current"></span>
            </div>}
            {/* Note: Using CSS shapes for menu icon to avoid importing another icon if not available, or I can use existing icons. 
                    Wait, I have Check, Copy, Terminal, Code2, Globe, Sparkles imported. I don't have Menu or X. 
                    I'll just use simple span lines for hamburger and Check rotated (or just X logic) for close. 
                    Actually, let's use the X icon if I can import it, or just styled spans.
                */}
          </button>
        </div>

        {/* Mobile Menu Overlay */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="absolute top-0 left-0 w-full bg-white border-b border-slate-200 shadow-xl p-4 pt-20 md:hidden flex flex-col gap-4 z-40"
            >
              {navLinks.map(link => (
                <a
                  key={link.name}
                  href={link.href}
                  className="text-lg font-medium text-slate-600 py-2 border-b border-slate-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.name}
                </a>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Hero Section */}
      <section className="w-full relative pt-12 md:pt-20 pb-0 md:pb-32 border-b border-black/5 dark:border-white/5 overflow-hidden">
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="flex flex-col items-start max-w-2xl"
            >
              <div className="mb-4 md:mb-6 font-mono text-blue-600 text-[10px] md:text-xs tracking-[0.2em] border border-blue-100 bg-blue-50 px-3 py-1 uppercase">
                The First of its Kind
              </div>

              <h1 className="text-4xl sm:text-5xl md:text-8xl font-bold tracking-tight text-slate-900 mb-6 leading-[0.9]">
                Program in your <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 font-gujarati">માતૃભાષા</span> (Mother Tongue).
              </h1>

              <p className="text-xl md:text-2xl text-slate-500 max-w-xl mb-10 font-light leading-relaxed">
                A complete Python implementation in Gujarati. Break the language barrier and build powerful software using the syntax you dream in.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 items-start">
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
                  <Button size="lg" className="relative h-14 px-8 text-lg bg-slate-900 border-none text-white hover:bg-slate-800">
                    Get Started <span className="ml-2 font-mono text-xs opacity-50">&rarr;</span>
                  </Button>
                </div>

                <Link href="/docs">
                  <Button size="lg" variant="outline" className="h-14 px-8 text-lg border-slate-200 text-slate-600 hover:text-blue-600 hover:border-blue-200 font-mono">
                    View Documentation
                  </Button>
                </Link>
              </div>
            </motion.div>

            {/* Right Side - Interactive Code Visual */}
            <div className="w-full flex justify-center lg:justify-end mt-12 lg:mt-0">
              <HeroCodeCard />
            </div>
          </div>
        </div>

        {/* Decorative Grid Element */}
        <div className="absolute top-0 right-0 w-1/3 h-full border-l border-black/5 hidden lg:block">
          <div className="h-full w-full bg-slate-50/30 flex items-center justify-center">
            <div className="text-[20rem] font-bold text-slate-100 select-none font-gujarati opacity-50 blur-3xl">અ</div>
          </div>
        </div>
      </section>

      {/* Installation Section */}
      <section id="install" className="w-full py-20 border-b border-black/5 bg-slate-50/50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-sm font-mono tracking-widest text-slate-400 mb-4">01 / INSTALLATION</h2>
              <h3 className="text-4xl font-bold text-slate-900 mb-6 font-gujarati">સ્થાપન (Installation)</h3>
              <p className="text-slate-600 mb-8 max-w-md">
                Get started instantly. Gujarati Python is available via PyPI and can be installed with a single command.
              </p>

              <div className="bg-white border border-slate-200 p-1 flex items-center justify-between shadow-sm max-w-md">
                <code className="px-4 py-3 font-mono text-sm text-slate-700">pip install gujarati-python</code>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={copyCommand}
                  className="h-10 w-10 p-0"
                >
                  {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4 text-slate-400" />}
                </Button>
              </div>
            </div>

            {/* Terminal Preview */}
            <div className="rounded-lg overflow-hidden bg-slate-950 shadow-2xl border border-slate-800 font-mono text-xs md:text-sm">
              <div className="flex items-center gap-2 px-4 py-3 bg-slate-900 border-b border-slate-800">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="ml-2 text-slate-500">bash</span>
              </div>
              <div className="p-6 text-slate-300 space-y-2">
                <div className="flex">
                  <span className="text-blue-500 mr-2">$</span>
                  <span className="text-white">gujarati-python example.py</span>
                </div>
                <div className="text-green-400">પરિણામ: 10</div>
                <div className="text-slate-500"># Process finished successfully</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="w-full py-24">
        <div className="container mx-auto px-4">
          <div className="flex items-end justify-between mb-16">
            <div>
              <h2 className="text-sm font-mono tracking-widest text-slate-400 mb-4">02 / FEATURES</h2>
              <h3 className="text-4xl font-bold text-slate-900">Why Gujarati Python?</h3>
            </div>
            <div className="hidden md:block w-px h-20 bg-slate-200 transform rotate-12"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 border-t border-l border-slate-200">
            {/* Feature 1 */}
            <div className="group border-r border-b border-slate-200 p-10 hover:bg-slate-50 transition-colors relative">
              <div className="absolute top-4 right-4 text-slate-200 group-hover:text-blue-200 transition-colors">
                <Terminal size={32} strokeWidth={1} />
              </div>
              <h4 className="font-bold text-xl mb-3 mt-4">Native Syntax</h4>
              <p className="text-slate-500 leading-relaxed text-sm">
                Write <code className="bg-slate-100 px-1 py-0.5 rounded text-blue-600">ડેફ</code> instead of <code className="bg-slate-100 px-1 py-0.5 rounded text-slate-600">def</code>. Complete language mapping for intuitive coding.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group border-r border-b border-slate-200 p-10 hover:bg-slate-50 transition-colors relative">
              <div className="absolute top-4 right-4 text-slate-200 group-hover:text-blue-200 transition-colors">
                <Code2 size={32} strokeWidth={1} />
              </div>
              <h4 className="font-bold text-xl mb-3 mt-4">Python Compatible</h4>
              <p className="text-slate-500 leading-relaxed text-sm">
                Built on top of standard Python (v3.12+). Use all your favorite libraries like NumPy and Pandas seamlessly.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group border-r border-b border-slate-200 p-10 hover:bg-slate-50 transition-colors relative">
              <div className="absolute top-4 right-4 text-slate-200 group-hover:text-blue-200 transition-colors">
                <Sparkles size={32} strokeWidth={1} />
              </div>
              <h4 className="font-bold text-xl mb-3 mt-4">Modern Tooling</h4>
              <p className="text-slate-500 leading-relaxed text-sm">
                Includes a custom CLI, REPL, and VS Code extension support for a modern developer experience.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* JSON-LD for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Gujarati Python",
            "operatingSystem": "Any",
            "applicationCategory": "DeveloperApplication",
            "offers": {
              "@type": "Offer",
              "price": "0",
              "priceCurrency": "USD",
            },
            "description": "The world's first complete Python programming environment in the Gujarati language.",
            "author": {
              "@type": "Person",
              "name": "Ritesh Rana",
              "url": "https://riteshrana.engineer"
            },
            "downloadUrl": "https://pypi.org/project/gujarati-python/",
            "featureList": "Native Gujarati Syntax, Python Compatibility, Modern Tooling",
            "softwareRequirements": "Python 3.12+"
          }),
        }}
      />

      {/* Footer */}
      <footer className="w-full py-12 border-t border-slate-200 bg-slate-50">
        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="text-sm font-mono text-slate-400">
            <p>© 2026 GUJARATI PYTHON</p>
            <p>DESIGNED FOR BUILDERS</p>
          </div>

          <div className="flex flex-col items-center md:items-end gap-2">
            <p className="text-sm font-mono text-slate-500">Made by <span className="font-bold text-slate-900">Ritesh Rana</span></p>
            <div className="flex gap-4">
              <a href="https://www.linkedin.com/in/riteshengineer/" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-blue-600 transition-colors">
                <span className="sr-only">LinkedIn</span>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path fillRule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="mailto:ritesh19@bu.edu" className="text-slate-400 hover:text-blue-600 transition-colors">
                <span className="sr-only">Email</span>
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                </svg>
              </a>
              <a href="https://github.com/ambicuity" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-blue-600 transition-colors">
                <span className="sr-only">GitHub</span>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
