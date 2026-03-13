#!/usr/bin/env python3
"""Keep the Contributors Hall of Fame in sync with merged PRs."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote


DEFAULT_COMMENT_USAGE = (
    "Usage: `@all-contributors please add @username for code` "
    "or `@all-contributors please add @username for code, doc`."
)

DEFAULT_CONFIG = {
    "repoType": "github",
    "repoHost": "https://github.com",
    "files": ["CONTRIBUTORS.md"],
    "imageSize": 100,
    "commit": False,
    "commitConvention": "none",
    "contributorsPerLine": 7,
}

CONTRIBUTION_ICONS = {
    "audio": "🔊",
    "blog": "📝",
    "bug": "🐛",
    "business": "💼",
    "code": "💻",
    "content": "🖋",
    "data": "🔣",
    "design": "🎨",
    "doc": "📖",
    "eventOrganizing": "📋",
    "example": "💡",
    "financial": "💵",
    "fundingFinding": "🔍",
    "ideas": "🤔",
    "infra": "🚇",
    "maintenance": "🚧",
    "mentoring": "🧑‍🏫",
    "platform": "📦",
    "plugin": "🔌",
    "projectManagement": "📆",
    "question": "💬",
    "research": "🔬",
    "review": "👀",
    "security": "🛡️",
    "talk": "📢",
    "test": "⚠️",
    "tests": "⚠️",
    "tool": "🔧",
    "translation": "🌍",
    "tutorial": "✅",
    "userTesting": "📓",
    "video": "📹",
}

PR_SEARCH_CONTRIBUTIONS = {
    "blog",
    "bug",
    "code",
    "content",
    "data",
    "design",
    "doc",
    "example",
    "ideas",
    "plugin",
    "research",
    "security",
    "test",
    "tests",
    "tool",
    "translation",
    "tutorial",
    "video",
}

COMMAND_PATTERN = re.compile(
    r"@all-contributors\s+(?:please\s+)?add\s+@?([A-Za-z0-9-]+)\s+for\s+(.+)",
    re.IGNORECASE,
)


@dataclass
class CommandParseResult:
    """Structured output for a Hall of Fame command comment."""

    valid: bool
    login: str = ""
    contributions: list[str] | None = None
    error_message: str = DEFAULT_COMMENT_USAGE


@dataclass
class UpsertResult:
    """Outcome of updating the Hall of Fame config."""

    changed: bool
    added: bool
    metadata_changed: bool
    new_contributions: list[str]


def parse_arguments() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_command = subparsers.add_parser(
        "parse-command",
        help="Parse a manual @all-contributors command comment.",
    )
    parse_command.add_argument(
        "--comment-body",
        required=True,
        help="Full comment body to inspect for a supported command.",
    )

    upsert = subparsers.add_parser(
        "upsert",
        help="Add or update a contributor in the Hall of Fame files.",
    )
    upsert.add_argument("--config", default=".all-contributorsrc")
    upsert.add_argument("--hall-of-fame", default="CONTRIBUTORS.md")
    upsert.add_argument("--owner", required=True)
    upsert.add_argument("--repo", required=True)
    upsert.add_argument("--login", required=True)
    upsert.add_argument("--name", default="")
    upsert.add_argument("--avatar-url", default="")
    upsert.add_argument("--profile", default="")
    upsert.add_argument(
        "--contribution",
        action="append",
        default=[],
        help="Contribution type to add. Can be repeated.",
    )
    upsert.add_argument(
        "--contributions-json",
        default="",
        help="JSON array of contribution types to add.",
    )

    return parser.parse_args()


def load_config(path: Path, owner: str, repo: str) -> tuple[dict[str, Any], bool]:
    """Load the contributors config and ensure required defaults exist."""

    if path.exists():
        config = json.loads(path.read_text(encoding="utf-8"))
        changed = False
    else:
        config = {}
        changed = True

    if not isinstance(config, dict):
        raise ValueError(f"{path} must contain a JSON object.")

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = list(value) if isinstance(value, list) else value
            changed = True

    if config.get("projectOwner") != owner:
        config["projectOwner"] = owner
        changed = True

    if config.get("projectName") != repo:
        config["projectName"] = repo
        changed = True

    files = config.setdefault("files", [])
    if not isinstance(files, list):
        raise ValueError("The files field must be a list.")
    if "CONTRIBUTORS.md" not in files:
        files.append("CONTRIBUTORS.md")
        changed = True

    contributors = config.setdefault("contributors", [])
    if not isinstance(contributors, list):
        raise ValueError("The contributors field must be a list.")

    return config, changed


def save_config(path: Path, config: dict[str, Any]) -> None:
    """Persist the contributors config in a stable JSON format."""

    path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def collect_contributions(args: argparse.Namespace) -> list[str]:
    """Merge repeated and JSON-form contributions into a unique list."""

    contributions = list(args.contribution)
    if args.contributions_json:
        json_values = json.loads(args.contributions_json)
        if not isinstance(json_values, list):
            raise ValueError("--contributions-json must be a JSON array.")
        contributions.extend(str(value) for value in json_values)

    unique_contributions = unique_case_insensitive(
        normalize_token(value) for value in contributions if normalize_token(value)
    )
    if not unique_contributions:
        raise ValueError("At least one contribution type is required.")
    return unique_contributions


def normalize_token(value: str) -> str:
    """Trim whitespace from a user-provided token."""

    return value.strip()


def normalize_login(login: str) -> str:
    """Normalize a GitHub login for comparisons."""

    return login.strip().casefold()


def unique_case_insensitive(values: Any) -> list[str]:
    """Return values in order, deduplicated case-insensitively."""

    unique_values: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.casefold()
        if key in seen:
            continue
        unique_values.append(value)
        seen.add(key)
    return unique_values


def parse_comment_command(comment_body: str) -> CommandParseResult:
    """Parse a supported manual Hall of Fame comment command."""

    for line in comment_body.splitlines():
        match = COMMAND_PATTERN.search(line.strip())
        if not match:
            continue

        login = match.group(1).strip()
        contribution_text = re.sub(
            r"\s+(?:and|&)\s+",
            ",",
            match.group(2).strip().rstrip(".!"),
            flags=re.IGNORECASE,
        )
        contributions = [
            normalize_token(part)
            for part in contribution_text.split(",")
            if normalize_token(part)
        ]
        contributions = unique_case_insensitive(contributions)
        if not contributions:
            break

        return CommandParseResult(
            valid=True,
            login=login,
            contributions=contributions,
            error_message="",
        )

    return CommandParseResult(valid=False)


def contributor_defaults(
    login: str,
    name: str,
    avatar_url: str,
    profile: str,
    contributions: list[str],
) -> dict[str, Any]:
    """Build a normalized contributor entry."""

    clean_login = login.strip()
    clean_name = name.strip() or clean_login
    clean_profile = profile.strip() or f"https://github.com/{clean_login}"
    clean_avatar = avatar_url.strip() or f"https://github.com/{clean_login}.png"

    return {
        "login": clean_login,
        "name": clean_name,
        "avatar_url": clean_avatar,
        "profile": clean_profile,
        "contributions": unique_case_insensitive(contributions),
    }


def upsert_contributor(
    config: dict[str, Any],
    *,
    login: str,
    name: str,
    avatar_url: str,
    profile: str,
    contributions: list[str],
) -> UpsertResult:
    """Add a contributor or enrich an existing one without duplication."""

    desired = contributor_defaults(login, name, avatar_url, profile, contributions)
    contributors = config.setdefault("contributors", [])
    normalized_login = normalize_login(login)

    for contributor in contributors:
        if normalize_login(str(contributor.get("login", ""))) != normalized_login:
            continue

        changed = False
        metadata_changed = False

        if contributor.get("login") != desired["login"]:
            contributor["login"] = desired["login"]
            changed = True
            metadata_changed = True

        raw_name = name.strip()
        raw_avatar_url = avatar_url.strip()
        raw_profile = profile.strip()

        metadata_candidates = {
            "name": raw_name or str(contributor.get("name", "")).strip() or desired["name"],
            "avatar_url": (
                raw_avatar_url
                or str(contributor.get("avatar_url", "")).strip()
                or desired["avatar_url"]
            ),
            "profile": raw_profile or str(contributor.get("profile", "")).strip() or desired["profile"],
        }

        for field, value in metadata_candidates.items():
            if contributor.get(field) != value:
                contributor[field] = value
                changed = True
                metadata_changed = True

        existing_contributions = [
            str(value) for value in contributor.get("contributions", []) if str(value).strip()
        ]
        existing_keys = {value.casefold() for value in existing_contributions}
        new_contributions: list[str] = []

        for contribution in desired["contributions"]:
            if contribution.casefold() in existing_keys:
                continue
            existing_contributions.append(contribution)
            existing_keys.add(contribution.casefold())
            new_contributions.append(contribution)
            changed = True

        contributor["contributions"] = existing_contributions

        return UpsertResult(
            changed=changed,
            added=False,
            metadata_changed=metadata_changed,
            new_contributions=new_contributions,
        )

    contributors.append(desired)
    return UpsertResult(
        changed=True,
        added=True,
        metadata_changed=False,
        new_contributions=list(desired["contributions"]),
    )


def contribution_icon(contribution: str) -> str:
    """Return the icon used for a contribution type."""

    return CONTRIBUTION_ICONS.get(contribution, contribution)


def contribution_link(contribution: str, login: str, profile: str, owner: str, repo: str) -> str:
    """Return a stable link for the contribution icon."""

    if contribution in PR_SEARCH_CONTRIBUTIONS:
        query = quote(f"is:pr author:{login}")
        return f"https://github.com/{owner}/{repo}/pulls?q={query}"
    return profile


def render_contributors_markdown(config: dict[str, Any], owner: str, repo: str) -> str:
    """Render the Hall of Fame markdown from the contributors config."""

    blocks: list[str] = []
    for contributor in config.get("contributors", []):
        login = str(contributor.get("login", "")).strip()
        if not login:
            continue

        name = str(contributor.get("name", "")).strip() or login
        profile = str(contributor.get("profile", "")).strip() or f"https://github.com/{login}"
        contributions = [
            str(value).strip()
            for value in contributor.get("contributions", [])
            if str(value).strip()
        ]

        lines = [f"[{name}]({profile})"]
        for contribution in contributions:
            icon = contribution_icon(contribution)
            link = contribution_link(contribution, login, profile, owner, repo)
            lines.append(f"[{icon}]({link})")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks) + ("\n" if blocks else "")


def write_hall_of_fame(path: Path, markdown: str) -> bool:
    """Write the Hall of Fame markdown if it changed."""

    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current == markdown:
        return False
    path.write_text(markdown, encoding="utf-8")
    return True


def emit_output(name: str, value: Any) -> None:
    """Emit GitHub Actions compatible step output."""

    print(f"{name}={value}")


def run_parse_command(comment_body: str) -> int:
    """CLI wrapper for comment command parsing."""

    result = parse_comment_command(comment_body)
    emit_output("valid", str(result.valid).lower())
    emit_output("login", result.login)
    emit_output(
        "contributions_json",
        json.dumps(result.contributions or [], ensure_ascii=False),
    )
    emit_output("error_message", result.error_message)
    return 0


def run_upsert(args: argparse.Namespace) -> int:
    """CLI wrapper for contributor upsert operations."""

    config_path = Path(args.config)
    hall_of_fame_path = Path(args.hall_of_fame)
    contributions = collect_contributions(args)
    config, config_changed = load_config(config_path, args.owner, args.repo)
    upsert_result = upsert_contributor(
        config,
        login=args.login,
        name=args.name,
        avatar_url=args.avatar_url,
        profile=args.profile,
        contributions=contributions,
    )

    if config_changed or upsert_result.changed:
        save_config(config_path, config)

    markdown = render_contributors_markdown(config, args.owner, args.repo)
    markdown_changed = write_hall_of_fame(hall_of_fame_path, markdown)
    changed = config_changed or upsert_result.changed or markdown_changed

    emit_output("changed", str(changed).lower())
    emit_output("added", str(upsert_result.added).lower())
    emit_output("metadata_changed", str(upsert_result.metadata_changed).lower())
    emit_output("new_contributions", ",".join(upsert_result.new_contributions))
    return 0


def main() -> int:
    """Entry point for Hall of Fame maintenance commands."""

    args = parse_arguments()
    if args.command == "parse-command":
        return run_parse_command(args.comment_body)
    if args.command == "upsert":
        return run_upsert(args)
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
