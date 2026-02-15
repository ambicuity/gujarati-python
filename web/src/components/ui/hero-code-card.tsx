"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { cn } from "../../lib/utils";

const codeSteps = [
    {
        lang: "Python (English)",
        code: `def greet(name):
    print(f"Hello, {name}!")

greet("World")`,
        highlightColor: "text-slate-500",
    },
    {
        lang: "Translating...",
        code: `...`,
        highlightColor: "text-blue-500",
    },
    {
        lang: "Gujarati Python",
        code: `ડેફ સ્વાગત(નામ):
    છાપો(f"નમસ્તે, {નામ}!")

સ્વાગત("દુનિયા")`,
        highlightColor: "text-blue-600",
    }
];

export function HeroCodeCard() {
    const [step, setStep] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            setStep((prev) => (prev + 1) % codeSteps.length);
        }, 4000);
        return () => clearInterval(timer);
    }, []);

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative w-full max-w-lg mx-auto lg:mx-0 lg:ml-auto"
        >
            {/* Abstract Decorative Elements */}
            <div className="absolute -top-12 -right-12 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl z-0 pointer-events-none"></div>
            <div className="absolute -bottom-12 -left-12 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl z-0 pointer-events-none"></div>

            {/* Card Container */}
            <div className="relative z-10 bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl shadow-2xl overflow-hidden backdrop-blur-sm">
                {/* Header */}
                <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
                    <div className="flex space-x-2">
                        <div className="w-3 h-3 rounded-full bg-red-400/80"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-400/80"></div>
                        <div className="w-3 h-3 rounded-full bg-green-400/80"></div>
                    </div>
                    <div className="text-xs font-mono text-slate-400 uppercase tracking-widest">
                        demo.py
                    </div>
                </div>

                {/* Code Area */}
                <div className="p-6 h-[200px] flex flex-col justify-center">
                    <div className="text-xs font-mono mb-2 text-slate-400 flex justify-between">
                        <span>Language:</span>
                        <motion.span
                            key={step}
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={cn("font-bold", codeSteps[step].highlightColor)}
                        >
                            {codeSteps[step].lang}
                        </motion.span>
                    </div>

                    <div className="relative font-mono text-sm md:text-base leading-relaxed bg-slate-50 dark:bg-slate-900 rounded-lg p-4 border border-slate-100 dark:border-slate-800">
                        <motion.pre
                            key={step}
                            initial={{ opacity: 0, filter: "blur(4px)" }}
                            animate={{ opacity: 1, filter: "blur(0px)" }}
                            transition={{ duration: 0.5 }}
                            className={cn("whitespace-pre-wrap", step === 2 ? "text-slate-900 font-medium" : "text-slate-600")}
                        >
                            {codeSteps[step].code}
                        </motion.pre>
                    </div>
                </div>

                {/* Progress Bar / Decor */}
                <div className="h-1 bg-slate-100 w-full overflow-hidden">
                    <motion.div
                        initial={{ x: "-100%" }}
                        animate={{ x: "0%" }}
                        transition={{ duration: 4, ease: "linear", repeat: Infinity }}
                        className="h-full bg-gradient-to-r from-transparent via-blue-500 to-transparent w-1/2"
                    />
                </div>
            </div>
        </motion.div>
    );
}
