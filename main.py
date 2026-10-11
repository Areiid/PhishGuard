#!/usr/bin/env python3
"""PhishGuard — check a URL or message on your computer, without sending it anywhere."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from checker.report import build_report
from checker.text_checks import analyze
from checker.url_checks import check_url

URL_EXAMPLES = ROOT / "examples" / "sample_urls.txt"
TEXT_EXAMPLES = ROOT / "examples" / "sample_messages.txt"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check a link or message for common phishing tricks. "
            "Nothing you paste is sent to a server."
        )
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="A link, or a quoted email/SMS (quotes are recommended)",
    )
    parser.add_argument("--url", dest="url_flag", help="Check only as a website address")
    parser.add_argument("--text", dest="text_flag", help="Check the wording of a message")
    parser.add_argument("--file", dest="file_path", help="Read a message from a text file")
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Run the practice links in examples/sample_urls.txt",
    )
    parser.add_argument(
        "--text-examples",
        action="store_true",
        help="Run the practice messages in examples/sample_messages.txt",
    )
    return parser.parse_args(argv)


def iter_example_urls(path: Path) -> list[str]:
    urls: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            urls.append(stripped)
    return urls


def iter_example_messages(path: Path) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "---":
            joined = "\n".join(current).strip()
            if joined and not joined.startswith("#"):
                blocks.append(joined)
            current = []
            continue
        if line.strip().startswith("#") and not current:
            continue
        current.append(line)
    joined = "\n".join(current).strip()
    if joined and not joined.startswith("#"):
        blocks.append(joined)
    return blocks


def print_run_hint() -> None:
    print("PhishGuard needs a link or a message to check.")
    print()
    print("  python3 main.py")
    print("  python3 main.py \"https://paypa1-secure-login.com\"")
    print("  python3 main.py --text \"Your account will be closed in 24 hours...\"")
    print("  python3 main.py --examples")
    print("  python3 main.py --text-examples")
    print()
    print("On this Mac, use python3 (not python).")


def prompt_for_input() -> str | None:
    print("PhishGuard — paste a suspicious link or message, then press Enter.")
    print("Or type  examples  /  text-examples   (q to quit).")
    print()
    try:
        entered = input("> ").strip()
    except EOFError:
        return None
    return entered


def run_url_examples() -> int:
    if not URL_EXAMPLES.exists():
        print(f"Could not find {URL_EXAMPLES}", file=sys.stderr)
        return 1
    for url in iter_example_urls(URL_EXAMPLES):
        print(build_report(url, check_url(url), kind="url"))
        print()
    return 0


def run_text_examples() -> int:
    if not TEXT_EXAMPLES.exists():
        print(f"Could not find {TEXT_EXAMPLES}", file=sys.stderr)
        return 1
    for message in iter_example_messages(TEXT_EXAMPLES):
        kind, findings = analyze(message)
        print(build_report(message, findings, kind=kind))
        print()
    return 0


def run_analysis(raw: str, force_url: bool = False) -> int:
    if force_url:
        print(build_report(raw, check_url(raw), kind="url"))
        return 0
    kind, findings = analyze(raw)
    print(build_report(raw, findings, kind=kind))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.examples:
        return run_url_examples()
    if args.text_examples:
        return run_text_examples()

    if args.file_path:
        path = Path(args.file_path).expanduser()
        if not path.is_file():
            print(f"Could not read file: {path}", file=sys.stderr)
            return 1
        return run_analysis(path.read_text(encoding="utf-8"))

    raw = args.text_flag or args.url_flag or args.text
    if raw:
        key = raw.lower()
        if key in {"examples", "example"}:
            return run_url_examples()
        if key in {"text-examples", "textexamples"}:
            return run_text_examples()
        return run_analysis(raw, force_url=bool(args.url_flag))

    if sys.stdin.isatty():
        entered = prompt_for_input()
        if not entered or entered.lower() in {"q", "quit", "exit"}:
            return 0
        if entered.lower() in {"examples", "example"}:
            return run_url_examples()
        if entered.lower() in {"text-examples", "textexamples"}:
            return run_text_examples()
        return run_analysis(entered)

    print_run_hint()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
