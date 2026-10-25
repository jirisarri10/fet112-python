from __future__ import annotations

import argparse
import json
import sys

from .client import FET112Client
from .errors import FET112Error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fet112", description="FET112 command-line client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="run a pre-action environment check")
    check.add_argument("destination", help="destination committed to the action hash")
    check.add_argument("--action", default="transfer")
    check.add_argument("--amount", default="unspecified")
    check.add_argument("--asset", default="FET")
    check.add_argument("--base-url", default="https://www.fet112.com")
    check.add_argument("--timeout", type=float, default=10.0)
    check.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "check":
        return 2

    try:
        result = FET112Client(base_url=args.base_url, timeout=args.timeout).pre_action_check(
            action=args.action,
            destination=args.destination,
            amount=args.amount,
            asset=args.asset,
        )
    except (FET112Error, ValueError) as exc:
        print(f"FET112 error: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(result.raw, indent=2, ensure_ascii=False))
        return 0

    print(f"Decision: {result.decision}")
    if result.decision_basis:
        print(f"Basis: {result.decision_basis}")
    if result.action_hash:
        print(f"Action hash: {result.action_hash}")
    if result.report_hash:
        print(f"Report hash: {result.report_hash}")
    print("Action-specific risk: NOT_EVALUATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
