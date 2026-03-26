"""Command-line interface for bg-test-data."""

import argparse
import sys
from typing import Any

from bg_test_data.export import to_csv, to_json
from bg_test_data.providers import BgTestData


def _build_kwargs(args: argparse.Namespace, fields: list[str]) -> dict[str, Any]:
    """Extract non-None keyword arguments from parsed args."""
    kwargs: dict[str, Any] = {}
    for field in fields:
        value = getattr(args, field, None)
        if value is not None:
            kwargs[field] = value
    return kwargs


# Maps command name -> (method name, list of arg fields to forward)
_COMMANDS: dict[str, tuple[str, list[str]]] = {
    "person": ("person", ["gender", "min_age", "max_age"]),
    "company": ("company", ["eik_length"]),
    "egn": ("egn", ["gender"]),
    "eik": ("eik", ["length"]),
    "iban": ("iban", []),
    "phone": ("phone", ["phone_type"]),
    "name": ("name", ["gender"]),
    "address": ("address", ["city"]),
}


def main(argv: list[str] | None = None) -> None:
    """Entry point for the bg-test-data CLI."""
    parser = argparse.ArgumentParser(
        prog="bg-test-data",
        description="Generate Bulgarian test data with valid checksums.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument(
        "--count", "-n", type=int, default=1, help="Number of records to generate (default: 1)."
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json).",
    )

    subparsers = parser.add_subparsers(dest="command", help="Data type to generate.")

    # person
    p_person = subparsers.add_parser("person", help="Generate a person.")
    p_person.add_argument("--gender", choices=["male", "female"], default=None)
    p_person.add_argument("--min-age", type=int, default=18)
    p_person.add_argument("--max-age", type=int, default=70)

    # company
    p_company = subparsers.add_parser("company", help="Generate a company.")
    p_company.add_argument("--eik-length", type=int, choices=[9, 13], default=9)

    # egn
    p_egn = subparsers.add_parser("egn", help="Generate an EGN.")
    p_egn.add_argument("--gender", choices=["male", "female"], default=None)

    # eik
    p_eik = subparsers.add_parser("eik", help="Generate an EIK.")
    p_eik.add_argument("--length", type=int, choices=[9, 13], default=9)

    # iban
    subparsers.add_parser("iban", help="Generate an IBAN.")

    # phone
    p_phone = subparsers.add_parser("phone", help="Generate a phone number.")
    p_phone.add_argument("--type", choices=["mobile", "landline"], default=None, dest="phone_type")

    # name
    p_name = subparsers.add_parser("name", help="Generate a name.")
    p_name.add_argument("--gender", choices=["male", "female"], default=None)

    # address
    p_address = subparsers.add_parser("address", help="Generate an address.")
    p_address.add_argument("--city", default=None)

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    bg = BgTestData(seed=args.seed)

    # Dispatch via command table
    method_name, fields = _COMMANDS[args.command]
    kwargs = _build_kwargs(args, fields)
    method = getattr(bg, method_name)
    results = [method(**kwargs) for _ in range(args.count)]

    # Output
    _print_results(results, args.format, args.count)


def _print_results(results: list[Any], fmt: str, count: int) -> None:
    """Format and print results to stdout."""
    if count == 1 and isinstance(results[0], str):
        if fmt == "json":
            print(to_json({"value": results[0]}))
        else:
            print(results[0])
    elif count == 1 and isinstance(results[0], dict):
        if fmt == "json":
            print(to_json(results[0]))
        else:
            print(to_csv(results[0]))
    elif all(isinstance(r, str) for r in results):
        if fmt == "json":
            print(to_json([{"value": r} for r in results]))
        else:
            for r in results:
                print(r)
    else:
        if fmt == "json":
            print(to_json(results))
        else:
            print(to_csv(results))
