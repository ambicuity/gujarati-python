# Requires: gh CLI authenticated (gh auth login)
set -euo pipefail

REPO="ambicuity/gujarati-python"
echo "🏷️  Creating labels for ${REPO}..."
echo ""

create_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh label create "${name}" \
      --repo "${REPO}" \
      --color "${color}" \
      --description "${description}" \
      --force 2>/dev/null; then
    echo "  ✅  ${name}"
  else
    echo "  ⚠️   ${name} — skipped (check gh auth or repo permissions)"
  fi
}

# ============================================================
echo "── Type Labels ──────────────────────────────────────"
create_label "bug"           "d73a4a"  "Something isn't working"
create_label "enhancement"   "a2eeef"  "New feature or request"
create_label "documentation" "0075ca"  "Improvements or additions to documentation"
create_label "architecture"  "e4e669"  "Major structural change proposal"
create_label "chore"         "fef2c0"  "Maintenance or housekeeping task"
create_label "security"      "ee0701"  "Security vulnerability or concern"

# ============================================================
echo ""
echo "── Status Labels ────────────────────────────────────"
create_label "needs-triage"    "ededed"  "Awaiting maintainer review and categorization"
create_label "status: in-progress"   "fbca04"  "Actively being worked on"
create_label "awaiting-response"  "d4c5f9"  "Waiting for the contributor to respond or update"
create_label "stale"           "cccccc"  "No activity in 30+ days"
create_label "blocked"         "b60205"  "Cannot proceed until a blocker is resolved"
create_label "help wanted"     "008672"  "Extra attention needed from the community"
create_label "good first issue" "7057ff" "Good for newcomers — welcoming entry point"
create_label "good first issue candidate" "e4e669" "Potential GFI — needs maintainer review before assignment"
create_label "plan-me"         "0075ca"  "Triggers CodeRabbit to generate an implementation plan"
create_label "duplicate"       "cfd3d7"  "This issue or PR already exists"
create_label "wontfix"         "ffffff"  "This will not be worked on"
create_label "merge-conflict"  "e11d48"  "This PR has merge conflicts that must be resolved"
create_label "automated pr"    "0e8a16"  "PR created by an automation (Dependabot, Actions bot)"

# ============================================================
echo ""
echo "── Component Labels ─────────────────────────────────"
create_label "frontend"           "0e8a16"  "Web UI and nextjs app"
create_label "core"               "5319e7"  "Gujarati parsing library code"

# ============================================================
echo ""
echo "── Priority Labels ──────────────────────────────────"
create_label "priority: critical" "b60205"  "Must fix immediately (data loss, CI broken, site down)"
create_label "priority: high"     "e11d48"  "Important — should be addressed this week"
create_label "priority: medium"   "f59e0b"  "Nice to have — scheduled for next cycle"
create_label "priority: low"      "94a3b8"  "Minor — backlog"

# ============================================================
echo ""
echo "── Difficulty Tier Labels ───────────────────────────"
create_label "beginner"      "c2e0c6"  "Requires some prior contribution experience; beyond GFI"
create_label "intermediate"  "ffd33d"  "Requires codebase familiarity; 2-3 functions involved"
create_label "advanced"      "e6192a"  "Requires deep parsing/lexing knowledge; high-impact change"
create_label "ci-cd"         "bfdadc"  "Changes to GitHub Actions workflows or CI configuration"

echo ""
echo "✅  Done! All labels have been processed for ${REPO}."
echo "    View them at: https://github.com/${REPO}/labels"
