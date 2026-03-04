# Security Policy

## Reporting a Vulnerability

**Please do NOT open a public GitHub Issue for security vulnerabilities.**

Opening a public issue exposes the vulnerability to all users — including malicious actors — before a patch is available.

### Private Disclosure Process

1. **Email the maintainer directly at:** `contact@riteshrana.engineer`
2. Use the subject line: `[SECURITY] Gujarati Python - <brief description>`
3. Include the following in your report:
   - A description of the vulnerability and its potential impact (e.g., Code Injection in parser, XSS in Web Playground)
   - Steps to reproduce the issue
   - Any proof-of-concept code
   - Your suggested fix (if you have one)

### What to Expect

| Timeline         | Action                                           |
| ---------------- | ------------------------------------------------ |
| Within 48 hours  | Acknowledgement of your report                   |
| Within 7 days    | Initial assessment and severity classification   |
| Within 30 days   | Patch released and CVE filed (if applicable)     |
| Post-patch       | Public disclosure with credit to the reporter    |

## Scope

The following are **in scope**:
- **Python parser** (`મુખ્ય.py`, `રંગોળી.py`): Arbitrary code execution during `eval` or translation mapping exploitation.
- **Web UI** (`web/`): Stored/Reflected XSS in the playground input area, or remote code execution via frontend-run logic.
- **GitHub Actions workflows**: Secrets exposure, supply-chain attacks.

## Best Practices
- **Do not introduce bare `eval()` or `exec()`** when handling user input without extremely strict sanitization.
- **Verify Dependency Updates**: If bumping an npm or pip package interactively, make sure it is not subject to a current CVE.
