<!--
  PR TITLE — READ BEFORE TYPING (bot will auto-reject if wrong)
  ─────────────────────────────────────────────────────────────
  Format:  <type>(<scope>): <short summary, lowercase, no period>

  Types:
    feat     – new feature or functionality
    fix      – bug fix
    docs     – documentation only
    test     – tests only, no production code
    chore    – maintenance (deps, CI, housekeeping)
    refactor – code change that is neither fix nor feature
    perf     – performance improvement

  Scopes (optional but recommended):
    core, parser, lexer, web, docs, tests, ci

  ✅ feat(core): add print statement translation
  ✅ fix(parser): handle string literals correctly
  ✅ test(core): add edge cases for boolean logic
  ✅ chore(ci): update dependabot config
  ✅ docs(readme): add setup instructions

  ❌ Update code            ← no type, no description
  ❌ Fixed the bug          ← no type, too vague
  ❌ feat: Added feature    ← capital letter, past tense

  Shortcut: title the PR "@coderabbitai" and the bot renames it correctly.
-->

## Linked Issue

Fixes #

## Summary

<!-- What changed and why? One or two sentences max. -->

## Changes Made

<!-- Which files changed and why? Delete rows that don't apply. -->

| File | What changed |
|------|-------------|
| `મુખ્ય.py` | |
| `રંગોળી.py` | |
| `ટેસ્ટ/` | |
| `web/` | |
| Other | |

## Testing

<!-- How did you verify this locally before pushing? -->

- [ ] `pytest` (or equivalent) — tests pass
- [ ] Manual test of the interpreter with a `.gpy` file
- [ ] Web frontend builds successfully (if changed)

## Notes for Reviewer

<!-- Anything non-obvious about the approach? Leave blank if straightforward. -->

---

> **📋 What is checked automatically by CI — you do not need to self-certify these:**
>
> | Check | Enforced by |
> |-------|-------------|
> | PR title follows Conventional Commits | `bot-pr-title-check` — auto-rejects on open |
> | PR links to an assigned issue | `bot-linked-issue-enforcer` + `bot-assignment-check` |
> | Auto-generated outputs not manually edited | `bot-pr-protected-files` — hard CI failure |
> | Security scan (CodeQL + Trivy) | `codeql.yml` + `trivy.yml` |
