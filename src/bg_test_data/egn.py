"""Bulgarian EGN (Unified Civil Number) generator and validator.

EGN structure: YYMMDDXXXC (10 digits)
- YY: year of birth (last 2 digits)
- MM: month with century encoding (+20 for 1800s, as-is for 1900s, +40 for 2000s)
- DD: day of birth
- XXX: birth order number (9th digit parity: even=male, odd=female)
- C: check digit (weights [2,4,8,5,10,9,7,3,6], sum mod 11, if 10 then 0)
"""

import calendar
from datetime import date
from typing import Literal

from bg_test_data._random import SeededRandom

Gender = Literal["male", "female"]

_EGN_WEIGHTS = [2, 4, 8, 5, 10, 9, 7, 3, 6]


def generate_egn(
    rng: SeededRandom,
    *,
    gender: Gender | None = None,
    birth_date: date | None = None,
    min_year: int = 1920,
    max_year: int = 2005,
) -> str:
    """Generate a valid Bulgarian EGN.

    Args:
        rng: Seeded random instance.
        gender: Force male or female. Random if None.
        birth_date: Specific birth date. Random if None.
        min_year: Minimum birth year (used when birth_date is None).
        max_year: Maximum birth year (used when birth_date is None).

    Returns:
        A 10-digit string representing a valid EGN.
    """
    if gender is None:
        gender = rng.choice(["male", "female"])

    if birth_date is None:
        year = rng.randint(min_year, max_year)
        month = rng.randint(1, 12)
        max_day = calendar.monthrange(year, month)[1]
        day = rng.randint(1, max_day)
        birth_date = date(year, month, day)

    year = birth_date.year
    month = birth_date.month
    day = birth_date.day

    yy = year % 100
    encoded_month = _encode_month(month, year)

    # Birth order number (3 digits, positions 6-8)
    # 9th digit (index 8) parity determines gender: even=male, odd=female
    order_base = rng.randint(0, 49)  # 0-49 range for the base
    order_num = order_base * 2  # Makes it even
    if gender == "female":
        order_num += 1  # Makes it odd

    # Pad to 3 digits (region code + order)
    region = rng.randint(0, 43)  # Region codes 0-43
    seq_digits = [region // 10, region % 10, order_num % 10]

    # Ensure gender bit is correct
    if gender == "male" and seq_digits[2] % 2 != 0 or gender == "female" and seq_digits[2] % 2 == 0:
        seq_digits[2] = (seq_digits[2] + 1) % 10

    digits = [
        yy // 10,
        yy % 10,
        encoded_month // 10,
        encoded_month % 10,
        day // 10,
        day % 10,
        seq_digits[0],
        seq_digits[1],
        seq_digits[2],
    ]

    check = _calculate_checksum(digits)
    digits.append(check)

    return "".join(str(d) for d in digits)


def validate_egn(egn: str) -> bool:
    """Validate a Bulgarian EGN.

    Args:
        egn: The EGN string to validate.

    Returns:
        True if the EGN is valid, False otherwise.
    """
    if len(egn) != 10 or not egn.isdigit():
        return False

    digits = [int(d) for d in egn]
    expected_check = _calculate_checksum(digits[:9])

    if digits[9] != expected_check:
        return False

    # Validate date
    try:
        parsed = parse_egn(egn)
        _ = parsed["birth_date"]
    except (ValueError, KeyError):
        return False

    return True


def parse_egn(egn: str) -> dict[str, object]:
    """Parse an EGN and extract information.

    Args:
        egn: A 10-digit EGN string.

    Returns:
        Dict with 'birth_date' (date), 'gender' (str), 'region' (int).

    Raises:
        ValueError: If the EGN format is invalid.
    """
    if len(egn) != 10 or not egn.isdigit():
        raise ValueError(f"EGN must be exactly 10 digits, got: {egn!r}")

    digits = [int(d) for d in egn]
    yy = digits[0] * 10 + digits[1]
    encoded_month = digits[2] * 10 + digits[3]
    day = digits[4] * 10 + digits[5]

    month, century_base = _decode_month(encoded_month)
    year = century_base + yy

    birth_date = date(year, month, day)
    gender: Gender = "male" if digits[8] % 2 == 0 else "female"
    region = digits[6] * 10 + digits[7]

    return {
        "birth_date": birth_date,
        "gender": gender,
        "region": region,
    }


def _calculate_checksum(digits: list[int]) -> int:
    """Calculate EGN check digit from first 9 digits."""
    total = sum(d * w for d, w in zip(digits[:9], _EGN_WEIGHTS, strict=False))
    remainder = total % 11
    return 0 if remainder == 10 else remainder


def _encode_month(month: int, year: int) -> int:
    """Encode month with century offset."""
    if 1800 <= year <= 1899:
        return month + 20
    elif 1900 <= year <= 1999:
        return month
    elif 2000 <= year <= 2099:
        return month + 40
    else:
        raise ValueError(f"Year {year} is out of supported range (1800-2099)")


def _decode_month(encoded_month: int) -> tuple[int, int]:
    """Decode encoded month to (actual_month, century_base)."""
    if 1 <= encoded_month <= 12:
        return encoded_month, 1900
    elif 21 <= encoded_month <= 32:
        return encoded_month - 20, 1800
    elif 41 <= encoded_month <= 52:
        return encoded_month - 40, 2000
    else:
        raise ValueError(f"Invalid encoded month: {encoded_month}")
