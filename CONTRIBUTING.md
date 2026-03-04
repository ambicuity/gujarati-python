# Contributing to ગુજરાતી પાઈથન (Gujarati Python)

First off — **thank you** for taking the time to contribute! 🎉

Gujarati Python is an open-source initiative to let developers write Python using native Gujarati keywords. Every contribution — whether fixing a parsing issue, extending the standard library mappings, or improving the Web Playground — directly helps lower the barrier to entry for coding.

---

## 1. Ways to Contribute
We organize work into clear tiers based on difficulty:

- [`good first issue`](https://github.com/ambicuity/gujarati-python/labels/good%20first%20issue) — Great for your first PR. Small, scoped, and well-defined tasks (e.g., adding a simple keyword mapping).
- [`beginner`](https://github.com/ambicuity/gujarati-python/labels/beginner) — Next step up. Single-file or logic-light fixes.
- [`intermediate`](https://github.com/ambicuity/gujarati-python/labels/intermediate) — Core AST or expression evaluation tweaks.
- [`advanced`](https://github.com/ambicuity/gujarati-python/labels/advanced) — Architectural changes to the lexer/parser loop.

**Non-coding contributions:**
- 🐛 **Bug reports** + ✨ **Feature Requests**: Use our [Issue Templates](https://github.com/ambicuity/gujarati-python/issues/new/choose).
- 📚 **Documentation**: Improvements to the README or tutorials.

---

## 2. The AI-Assisted Workflow
We use **CodeRabbit** for code reviews and architecture planning.

1. **Open an Issue**: Explain the bug or feature request. Let the maintainer assign it a tier.
2. **Use the `plan-me` label**: If you want AI assistance, add the `plan-me` label to the issue to get an auto-generated implementation plan.
3. **Write the Code**: Stick to the plan. Ensure tests run.
4. **Open a PR**: You **must** link the PR to the issue (`Fixes #123`).
5. **CodeRabbit Review**: Coderabbit will review the PR for correctness and security before the maintainer merges it.

---

## 3. Local Development Setup

### System Requirements
- Python 3.11+
- Node.js 20+ (if working on the web frontend)

### Installation
1. Fork and clone the repository.
2. Ensure you are on the `main` branch.
3. Run `pytest` to verify the core Python engine tests pass.
4. If editing the Web UI, navigate to `web/` and run `npm install`, then `npm run dev`.

### Code Style
- Python: PEP8 compliant. Add type hints to new definitions.
- Web: Standard React/Next.js conventions.

---

## 4. Automation Commands

You can interact with our repository bots via PR/Issue comments:
- `/assign` — Auto-assigns the issue to yourself.
- `@coderabbitai review` — Forces CodeRabbit to re-review the PR manually.
