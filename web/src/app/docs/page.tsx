"use client";

import { motion } from "framer-motion";
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { KEYWORD_MAP, BUILTIN_MAP, MODULE_MAP, TURTLE_MAP, MATH_MAP } from "../../lib/gujarati-mapping";
import { Copy, Check, Menu, X, ArrowLeft } from "lucide-react";
import { useState } from "react";
import Link from "next/link";

// Inline util to avoid import issues
function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

export default function DocsPage() {
    const [activeSection, setActiveSection] = useState("keywords");
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [copiedKey, setCopiedKey] = useState<string | null>(null);

    const handleCopy = (text: string, key: string) => {
        navigator.clipboard.writeText(text);
        setCopiedKey(key);
        setTimeout(() => setCopiedKey(null), 2000);
    };

    const sections = [
        { id: "keywords", title: "Keywords (કીવર્ડ્સ)" },
        { id: "builtins", title: "Built-in Functions (ફંક્શન્સ)" },
        { id: "modules", title: "Modules (મોડ્યુલ્સ)" },
        { id: "turtle", title: "Turtle Graphics (કાચબો)" },
        { id: "math", title: "Math Module (ગણિત)" },
    ];

    const renderTable = (data: Record<string, string>, title: string) => (
        <div className="mb-12 scroll-mt-24" id={title.toLowerCase().split(' ')[0]}>
            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
                <span className="w-8 h-[1px] bg-blue-600"></span>
                {title}
            </h2>
            <div className="rounded-lg border border-slate-200 overflow-hidden bg-white shadow-sm">
                <div className="grid grid-cols-2 bg-slate-50 border-b border-slate-200 p-4 font-mono text-sm text-slate-500 tracking-wider uppercase">
                    <div>Gujarati</div>
                    <div>English (Python)</div>
                </div>
                <div className="divide-y divide-slate-100">
                    {Object.entries(data).map(([guj, eng], idx) => (
                        <div
                            key={guj}
                            className="grid grid-cols-2 p-4 hover:bg-slate-50 transition-colors group items-center"
                        >
                            <div className="font-mono font-medium text-slate-900 font-gujarati text-lg">{guj}</div>
                            <div className="font-mono text-slate-600 flex items-center justify-between group-hover:text-blue-600">
                                <span>{eng}</span>
                                <button
                                    onClick={() => handleCopy(guj, guj)}
                                    className="opacity-0 group-hover:opacity-100 p-1.5 rounded hover:bg-blue-50 text-blue-600 transition-all"
                                    title="Copy Gujarati Keyword"
                                >
                                    {copiedKey === guj ? <Check size={14} /> : <Copy size={14} />}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );

    const scrollToSection = (id: string) => {
        setActiveSection(id);
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
        setMobileMenuOpen(false);
    };

    return (
        <main className="min-h-screen bg-white">
            {/* Navbar for Docs */}
            <nav className="w-full border-b border-black/5 bg-white/50 backdrop-blur-md sticky top-0 z-50">
                <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="p-2 -ml-2 text-slate-400 hover:text-slate-900 transition-colors">
                            <ArrowLeft size={20} />
                        </Link>
                        <div className="font-mono text-sm tracking-widest text-blue-600 font-bold">
                            GUJARATI_PYTHON <span className="text-slate-400 font-normal">/ DOCS</span>
                        </div>
                    </div>

                    <button
                        className="md:hidden p-2 text-slate-600"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    >
                        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </nav>

            <div className="container mx-auto px-4 flex items-start pt-8 pb-24 gap-12">
                {/* Sidebar Navigation */}
                <aside className={cn(
                    "fixed md:sticky top-20 left-0 h-[calc(100vh-5rem)] w-64 bg-white md:bg-transparent z-40 transform transition-transform duration-300 ease-in-out border-r md:border-none border-slate-200 p-6 md:p-0 overflow-y-auto",
                    mobileMenuOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
                )}>
                    <div className="space-y-1">
                        <h3 className="font-mono text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 px-3">
                            Contents
                        </h3>
                        {sections.map((section) => (
                            <button
                                key={section.id}
                                onClick={() => scrollToSection(section.id)}
                                className={cn(
                                    "w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-all font-mono",
                                    activeSection === section.id
                                        ? "bg-blue-50 text-blue-700"
                                        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                                )}
                            >
                                {section.title}
                            </button>
                        ))}
                    </div>
                </aside>

                {/* Main Content */}
                <div className="flex-1 w-full max-w-4xl mx-auto min-w-0">
                    <div id="keywords" className="scroll-mt-24">
                        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-2xl p-8 mb-12">
                            <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4 font-gujarati">
                                દસ્તાવેજીકરણ (Documentation)
                            </h1>
                            <p className="text-lg text-slate-600 leading-relaxed">
                                A complete reference for mapping standard English Python keywords to their Gujarati counterparts.
                                Use this guide to translate your mental models into native code.
                            </p>
                        </div>

                        {renderTable(KEYWORD_MAP, "Keywords")}
                    </div>

                    <div id="builtins" className="scroll-mt-24">
                        {renderTable(BUILTIN_MAP, "Built-in Functions")}
                    </div>

                    <div id="modules" className="scroll-mt-24">
                        {renderTable(MODULE_MAP, "Modules")}
                    </div>

                    <div id="turtle" className="scroll-mt-24">
                        {renderTable(TURTLE_MAP, "Turtle Graphics")}
                    </div>

                    <div id="math" className="scroll-mt-24">
                        {renderTable(MATH_MAP, "Math Module")}
                    </div>

                    <footer className="mt-20 pt-10 border-t border-slate-100 text-center text-slate-400 font-mono text-xs">
                        <p>Found a missing translation? <a href="https://github.com/ambicuity/gujarati-python" className="text-blue-600 hover:underline">Contribute on GitHub</a></p>
                    </footer>
                </div>
            </div>

            {/* Backdrop for mobile menu */}
            {mobileMenuOpen && (
                <div
                    className="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 md:hidden"
                    onClick={() => setMobileMenuOpen(false)}
                />
            )}
        </main>
    );
}
