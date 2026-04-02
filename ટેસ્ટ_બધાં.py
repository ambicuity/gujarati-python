#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""સંપૂર્ણ pytest ટેસ્ટ સ્યુટ - ગુજરાતી પાઈથન."""

import locale
import os
import platform
import subprocess
import sys
from pathlib import Path

from અનુવાદક import કોડ_અનુવાદ_કરો


import pytest


def _project_root() -> Path:
    return Path(__file__).parent


def _main_script() -> Path:
    return _project_root() / "મુખ્ય.py"


def _run_cli(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    return subprocess.run(
        [sys.executable, str(_main_script()), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(_project_root()),
        timeout=timeout,
        env=env,
    )


def test_platform_info_is_available() -> None:
    assert platform.system()
    assert platform.machine()
    assert sys.version
    assert sys.getdefaultencoding() == "utf-8"

    try:
        current_locale = locale.getlocale()
    except Exception:
        current_locale = None

    assert current_locale is None or isinstance(current_locale, tuple)


@pytest.mark.parametrize(
    "args, expected",
    [
        (["--help"], "ગુજરાતી પાઈથન"),
        (["--keywords"], "છાપો"),
        (["--search", "છાપો"], "છાપો"),
    ],
)
def test_cli_core_commands(args: list[str], expected: str) -> None:
    result = _run_cli(args)
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout


def test_run_simple_demo() -> None:
    result = _run_cli(["ઉદાહરણો/સરળ_ડેમો.py"])
    assert result.returncode == 0, result.stderr
    assert "ગુજરાતી પાઈથન" in result.stdout


def test_translate_simple_demo() -> None:
    result = _run_cli(["--translate", "ઉદાહરણો/સરળ_ડેમો.py"])
    assert result.returncode == 0, result.stderr
    assert "print(" in result.stdout


def test_turtle_વર્તુળ_mapping():
   
    code = """
            t = turtle.Turtle()
            t.વર્તુળ(50)
           """

    translated = કોડ_અનુવાદ_કરો(code)

    assert "turtle.circle(50)" in translated