"""Bulgarian BULSTAT/EIK generator and validator.

EIK structure:
- 9-digit: weights [1,2,3,4,5,6,7,8] on first 8 digits, sum mod 11.
  If result is 10, re-weight with [3,4,5,6,7,8,9,10]. Check digit = result mod 10.
- 13-digit: first 9 validated as above. Digits 9-12 weighted by [2,7,3,5],
  sum mod 11. If 10, re-weight with [4,9,5,7]. Final digit = result mod 10.
"""

from typing import Literal

from bg_test_data._random import SeededRandom

EikLength = Literal[9, 13]

_WEIGHTS_9_PRIMARY = [1, 2, 3, 4, 5, 6, 7, 8]
_WEIGHTS_9_SECONDARY = [3, 4, 5, 6, 7, 8, 9, 10]
_WEIGHTS_13_PRIMARY = [2, 7, 3, 5]
_WEIGHTS_13_SECONDARY = [4, 9, 5, 7]


def generate_eik(
    rng: SeededRandom,
    *,
    length: EikLength = 9,
) -> str:
    """Generate a valid Bulgarian EIK/BULSTAT number.

    Args:
        rng: Seeded random instance.
        length: 9 for companies, 13 for branches.

    Returns:
        A string of 9 or 13 digits representing a valid EIK.
    """
    # Generate first 8 random digits
    digits = [rng.randint(0, 9) for _ in range(8)]

    # Calculate 9th digit (check digit for 9-digit EIK)
    check9 = _calculate_eik9_checksum(digits)
    digits.append(check9)

    if length == 13:
        # Generate 3 more random digits (positions 9-11)
        extra = [rng.randint(0, 9) for _ in range(3)]
        digits.extend(extra)

        # Calculate 13th digit
        check13 = _calculate_eik13_checksum(digits)
        digits.append(check13)

    return "".join(str(d) for d in digits)


def validate_eik(eik: str) -> bool:
    """Validate a Bulgarian EIK/BULSTAT number.

    Args:
        eik: The EIK string to validate.

    Returns:
        True if the EIK is valid, False otherwise.
    """
    if not eik.isdigit():
        return False

    if len(eik) not in (9, 13):
        return False

    digits = [int(d) for d in eik]

    # Validate 9-digit checksum
    expected_check9 = _calculate_eik9_checksum(digits[:8])
    if digits[8] != expected_check9:
        return False

    # If 13-digit, validate additional checksum
    if len(eik) == 13:
        expected_check13 = _calculate_eik13_checksum(digits[:12])
        if digits[12] != expected_check13:
            return False

    return True


def _calculate_eik9_checksum(digits: list[int]) -> int:
    """Calculate the 9th digit checksum for EIK."""
    total = sum(d * w for d, w in zip(digits[:8], _WEIGHTS_9_PRIMARY, strict=False))
    remainder = total % 11

    if remainder == 10:
        total = sum(d * w for d, w in zip(digits[:8], _WEIGHTS_9_SECONDARY, strict=False))
        remainder = total % 11

    return remainder % 10


def _calculate_eik13_checksum(digits: list[int]) -> int:
    """Calculate the 13th digit checksum for EIK."""
    # Use digits at positions 8-11 (0-indexed)
    subset = digits[8:12]
    total = sum(d * w for d, w in zip(subset, _WEIGHTS_13_PRIMARY, strict=False))
    remainder = total % 11

    if remainder == 10:
        total = sum(d * w for d, w in zip(subset, _WEIGHTS_13_SECONDARY, strict=False))
        remainder = total % 11

    return remainder % 10
