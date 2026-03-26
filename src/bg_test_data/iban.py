"""Bulgarian IBAN generator and validator.

IBAN structure: BGcc BBBB SSSS TT AAAAAAAA (22 characters total)
- BG: country code
- cc: 2-digit check digits (mod-97 per ISO 13616)
- BBBB: 4-letter bank code (BIC)
- SSSS: 4-digit branch code
- TT: 2-digit account type
- AAAAAAAA: 8-digit account number
"""

from bg_test_data._data.bank_codes import BANK_CODES
from bg_test_data._random import SeededRandom

_COUNTRY_CODE = "BG"


def generate_iban(
    rng: SeededRandom,
    *,
    bank_code: str | None = None,
) -> str:
    """Generate a valid Bulgarian IBAN.

    Args:
        rng: Seeded random instance.
        bank_code: Specific 4-letter bank code. Random if None.

    Returns:
        A 22-character string representing a valid Bulgarian IBAN.
    """
    if bank_code is None:
        bank_code = rng.choice(list(BANK_CODES.keys()))
    else:
        bank_code = bank_code.upper()
        if len(bank_code) != 4 or not bank_code.isalpha():
            raise ValueError(f"bank_code must be exactly 4 letters, got: {bank_code!r}")

    # Branch code: 4 digits
    branch = "".join(str(rng.randint(0, 9)) for _ in range(4))

    # Account type: 2 digits
    account_type = "".join(str(rng.randint(0, 9)) for _ in range(2))

    # Account number: 8 digits
    account_number = "".join(str(rng.randint(0, 9)) for _ in range(8))

    # BBAN = bank_code + branch + account_type + account_number
    bban = bank_code + branch + account_type + account_number

    # Calculate check digits
    check_digits = _calculate_check_digits(bban)

    return f"{_COUNTRY_CODE}{check_digits}{bban}"


def validate_iban(iban: str) -> bool:
    """Validate a Bulgarian IBAN using mod-97 check.

    Args:
        iban: The IBAN string to validate (with or without spaces).

    Returns:
        True if the IBAN is valid, False otherwise.
    """
    iban = iban.replace(" ", "").upper()

    if len(iban) != 22:
        return False

    if not iban.startswith("BG"):
        return False

    # Check that positions 2-3 are digits (check digits)
    if not iban[2:4].isdigit():
        return False

    # Check that positions 4-7 are letters (bank code)
    if not iban[4:8].isalpha():
        return False

    # Check remaining positions are alphanumeric
    if not iban[8:].isalnum():
        return False

    # Mod-97 validation
    numeric = _iban_to_numeric(iban)
    return numeric % 97 == 1


def format_iban(iban: str, separator: str = " ") -> str:
    """Format an IBAN with separators every 4 characters.

    Args:
        iban: Raw IBAN string without spaces.
        separator: Separator character (default: space).

    Returns:
        Formatted IBAN string.
    """
    iban = iban.replace(" ", "")
    return separator.join(iban[i : i + 4] for i in range(0, len(iban), 4))


def _calculate_check_digits(bban: str) -> str:
    """Calculate IBAN check digits for a Bulgarian BBAN."""
    # Rearrange: BBAN + country_code + "00"
    rearranged = bban + _COUNTRY_CODE + "00"
    numeric = _string_to_numeric(rearranged)
    check = 98 - (numeric % 97)
    return f"{check:02d}"


def _iban_to_numeric(iban: str) -> int:
    """Convert IBAN to numeric for mod-97 validation.

    Move first 4 chars to end, then replace letters with numbers.
    """
    rearranged = iban[4:] + iban[:4]
    return _string_to_numeric(rearranged)


def _string_to_numeric(s: str) -> int:
    """Replace letters with numbers (A=10, B=11, ..., Z=35) and return integer."""
    result = []
    for char in s:
        if char.isdigit():
            result.append(char)
        else:
            result.append(str(ord(char.upper()) - ord("A") + 10))
    return int("".join(result))
