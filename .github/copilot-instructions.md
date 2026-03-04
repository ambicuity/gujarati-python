# Copilot Instructions — ગુજરાતી પાઈથન (Gujarati Python)

You are an expert AI software engineer assisting with **Gujarati Python**, a translated programming language bridging Gujarati text into executable Python or JavaScript.

## 1. Repository Identity
- **Goal:** Enable programming natively in Gujarati. Users write `.gpy` files which convert to `.py` via dictionary mapping, or run in the browser via Next.js for a web playground.
- **Tech Stack:** Python 3 (core engine), Next.js + React (web UI), standard libraries.
- **Maintainer:** Ritesh (@ambicuity), solo maintainer.

## 2. Architectural Constraints (Hard Rules)
- **Zero Hallucination with Dictionary Mappings:** Do NOT invent Gujarati keywords. Always refer to established structures when translating (`જો` -> `if`, `છાપો` -> `print`, etc.).
- **UTF-8 Enforcement:** All interactions with scripts and source code must handle UTF-8/Gujarati characters natively.
- **Separation of Concerns:** The core parsing logic must remain independent of the Web UI logic. The core should operate primarily in Python.

## 3. Code Standards
- Use **Conventional Commits** for all PR titles (`feat:`, `fix:`, `chore:`, `docs:`, `test:`).
- Document non-obvious unicode-handling code explicitly.
- **No force-pushing to main.**
- All code must survive CodeQL and Trivy security scans.

## 4. Testing Requirements
- Unit tests required for core logic (lexing, translating, evaluating).
- Pytest is preferred for Python testing.
- UI changes need to not break the `deploy-docs.yml` CI workflow.

## 5. Pre-commit & CI
- The project relies on deep automated CI. Ensure your suggestions do not bypass automation (e.g. don't suggest manually editing generated `web/out/` artifacts).

## 6. AI Interoperability & CodeRabbit Synergy
CodeRabbit will review PRs. When acting as an agent drafting code:
1. Output production-ready, clean, PEP8/ESLint compliant code.
2. Ensure you add `CHANGELOG.md` lines for feature work.
3. Don't write code that requires immediate heavy refactoring.
