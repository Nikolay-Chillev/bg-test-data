"""Export utilities for converting generated data to various formats."""

import csv
import io
import json
from typing import Any

DataType = dict[str, Any] | list[dict[str, Any]]


def to_dict(data: DataType) -> DataType:
    """Ensure data is a plain dict/list (identity for already-dict data).

    Args:
        data: A dict or list of dicts.

    Returns:
        The same data structure (useful as a no-op normalizer in pipelines).
    """
    return data


def to_json(
    data: DataType,
    *,
    indent: int = 2,
    ensure_ascii: bool = False,
) -> str:
    """Serialize data to a JSON string.

    Args:
        data: A dict or list of dicts.
        indent: JSON indentation level.
        ensure_ascii: If False (default), allow non-ASCII characters.

    Returns:
        A JSON-formatted string.
    """
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=str)


def to_csv(data: DataType) -> str:
    """Serialize data to a CSV string.

    Args:
        data: A dict (single row) or list of dicts.

    Returns:
        A CSV-formatted string with header row.
    """
    rows = [data] if isinstance(data, dict) else data

    if not rows:
        return ""

    # Flatten nested dicts with dot notation for CSV
    flat_rows = [_flatten_dict(row) for row in rows]

    # Collect all keys preserving order
    fieldnames: list[str] = []
    for row in flat_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(flat_rows)

    return output.getvalue()


def to_csv_file(data: DataType, filepath: str) -> None:
    """Write data to a CSV file.

    Args:
        data: A dict (single row) or list of dicts.
        filepath: Path to the output CSV file.
    """
    csv_string = to_csv(data)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        f.write(csv_string)


def _flatten_dict(d: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict[str, str]:
    """Flatten a nested dict using dot notation for keys.

    Example:
        {"address": {"city": "Sofia"}} -> {"address.city": "Sofia"}
    """
    items: list[tuple[str, str]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v) if v is not None else ""))
    return dict(items)
