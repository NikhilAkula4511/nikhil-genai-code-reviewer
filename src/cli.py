"""CLI for code review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from src.providers import review_code


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="GenAI code review")
    parser.add_argument("--file", required=True)
    parser.add_argument("--language", default="python")
    parser.add_argument("--provider", default=None)
    args = parser.parse_args()

    code = Path(args.file).read_text(encoding="utf-8")
    result = review_code(code, args.language, args.provider)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
