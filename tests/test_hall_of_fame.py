from __future__ import annotations

import json
from pathlib import Path

from scripts.hall_of_fame import (
    parse_comment_command,
    render_contributors_markdown,
    run_upsert,
    upsert_contributor,
)


def make_config() -> dict[str, object]:
    return {
        "projectName": "gujarati-python",
        "projectOwner": "ambicuity",
        "repoType": "github",
        "repoHost": "https://github.com",
        "files": ["CONTRIBUTORS.md"],
        "imageSize": 100,
        "commit": False,
        "commitConvention": "none",
        "contributorsPerLine": 7,
        "contributors": [
            {
                "login": "ambicuity",
                "name": "Ritesh Rana",
                "avatar_url": "https://avatars.githubusercontent.com/u/44251619?v=4",
                "profile": "https://github.com/ambicuity",
                "contributions": [
                    "code",
                    "infra",
                    "doc",
                    "maintenance",
                    "ideas",
                ],
            }
        ],
    }


def test_parse_comment_command_accepts_multiple_types() -> None:
    result = parse_comment_command(
        "@all-contributors please add @AhmedIkram05 for code, doc and ideas."
    )

    assert result.valid is True
    assert result.login == "AhmedIkram05"
    assert result.contributions == ["code", "doc", "ideas"]


def test_parse_comment_command_rejects_invalid_input() -> None:
    result = parse_comment_command("@all-contributors please add @AhmedIkram05")

    assert result.valid is False
    assert "Usage:" in result.error_message


def test_upsert_contributor_adds_new_login_once() -> None:
    config = make_config()

    result = upsert_contributor(
        config,
        login="AhmedIkram05",
        name="Ahmed Ikram",
        avatar_url="https://github.com/AhmedIkram05.png",
        profile="https://github.com/AhmedIkram05",
        contributions=["code"],
    )

    assert result.added is True
    assert result.new_contributions == ["code"]
    assert len(config["contributors"]) == 2


def test_upsert_contributor_updates_case_insensitively_without_duplicates() -> None:
    config = make_config()
    config["contributors"].append(
        {
            "login": "ahmedikram05",
            "name": "Ahmed",
            "avatar_url": "",
            "profile": "",
            "contributions": ["doc", "code"],
        }
    )

    first = upsert_contributor(
        config,
        login="AhmedIkram05",
        name="Ahmed Ikram",
        avatar_url="https://github.com/AhmedIkram05.png",
        profile="https://github.com/AhmedIkram05",
        contributions=["code", "ideas"],
    )
    second = upsert_contributor(
        config,
        login="AhmedIkram05",
        name="Ahmed Ikram",
        avatar_url="https://github.com/AhmedIkram05.png",
        profile="https://github.com/AhmedIkram05",
        contributions=["code", "ideas"],
    )

    assert first.added is False
    assert first.new_contributions == ["ideas"]
    assert second.changed is False

    ahmed = config["contributors"][1]
    assert ahmed["login"] == "AhmedIkram05"
    assert ahmed["contributions"] == ["doc", "code", "ideas"]
    assert ahmed["name"] == "Ahmed Ikram"


def test_upsert_contributor_preserves_existing_metadata_when_lookup_is_blank() -> None:
    config = make_config()
    config["contributors"].append(
        {
            "login": "AhmedIkram05",
            "name": "Ahmed Ikram",
            "avatar_url": "https://github.com/AhmedIkram05.png",
            "profile": "https://github.com/AhmedIkram05",
            "contributions": ["code"],
        }
    )

    result = upsert_contributor(
        config,
        login="AhmedIkram05",
        name="",
        avatar_url="",
        profile="",
        contributions=["code"],
    )

    assert result.changed is False
    assert config["contributors"][1]["name"] == "Ahmed Ikram"


def test_render_contributors_markdown_uses_profile_and_pr_links() -> None:
    config = make_config()
    config["contributors"].append(
        {
            "login": "AhmedIkram05",
            "name": "Ahmed Ikram",
            "avatar_url": "https://github.com/AhmedIkram05.png",
            "profile": "https://github.com/AhmedIkram05",
            "contributions": ["code", "maintenance", "customType"],
        }
    )

    markdown = render_contributors_markdown(config, "ambicuity", "gujarati-python")

    assert "[Ahmed Ikram](https://github.com/AhmedIkram05)" in markdown
    assert (
        "[💻](https://github.com/ambicuity/gujarati-python/pulls?q=is%3Apr%20author%3AAhmedIkram05)"
        in markdown
    )
    assert "[🚧](https://github.com/AhmedIkram05)" in markdown
    assert "[customType](https://github.com/AhmedIkram05)" in markdown


def test_run_upsert_updates_real_files_end_to_end(tmp_path: Path) -> None:
    config_path = tmp_path / ".all-contributorsrc"
    hall_of_fame_path = tmp_path / "CONTRIBUTORS.md"
    config_path.write_text(
        json.dumps(make_config(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    hall_of_fame_path.write_text("", encoding="utf-8")

    class Args:
        command = "upsert"
        config = str(config_path)
        hall_of_fame = str(hall_of_fame_path)
        owner = "ambicuity"
        repo = "gujarati-python"
        login = "AhmedIkram05"
        name = ""
        avatar_url = ""
        profile = ""
        contribution = ["code"]
        contributions_json = ""

    exit_code = run_upsert(Args())

    assert exit_code == 0

    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["contributors"][-1]["name"] == "AhmedIkram05"
    assert config["contributors"][-1]["profile"] == "https://github.com/AhmedIkram05"

    hall_of_fame = hall_of_fame_path.read_text(encoding="utf-8")
    assert "[AhmedIkram05](https://github.com/AhmedIkram05)" in hall_of_fame
