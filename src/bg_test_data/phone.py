"""Bulgarian phone number generator."""

from typing import Literal

from bg_test_data._data.cities import CITIES
from bg_test_data._random import SeededRandom

PhoneType = Literal["mobile", "landline"]


def generate_phone(
    rng: SeededRandom,
    *,
    phone_type: PhoneType | None = None,
    international: bool = True,
) -> str:
    """Generate a Bulgarian phone number.

    Args:
        rng: Seeded random instance.
        phone_type: Force 'mobile' or 'landline'. Random if None.
        international: If True, use +359 prefix. If False, use 0 prefix.

    Returns:
        A formatted Bulgarian phone number string.
    """
    if phone_type is None:
        phone_type = rng.choice(["mobile", "landline"])

    if phone_type == "mobile":
        return _generate_mobile(rng, international)
    else:
        return _generate_landline(rng, international)


def _generate_mobile(rng: SeededRandom, international: bool) -> str:
    """Generate a Bulgarian mobile phone number."""
    prefix = rng.choice(["87", "88", "89"])
    # Mobile: prefix + 7 digits (total 9 digits after country code)
    subscriber = prefix + str(rng.randint(0, 9))  # 3rd digit of operator prefix
    remaining = "".join(str(rng.randint(0, 9)) for _ in range(6))
    number = subscriber + remaining

    if international:
        return f"+359 {number[:2]} {number[2:5]} {number[5:]}"
    else:
        return f"0{number[:2]} {number[2:5]} {number[5:]}"


def _generate_landline(rng: SeededRandom, international: bool) -> str:
    """Generate a Bulgarian landline phone number."""
    city = rng.choice(CITIES)
    area_code = city[3]  # area_code from tuple

    # Remove leading 0 from area code for international format
    area_clean = area_code.lstrip("0")

    # Landline subscriber number length depends on area code length
    # Total national number is typically 8-9 digits (area code + subscriber)
    if len(area_code) <= 2:
        # Sofia: area code "02", subscriber 7 digits
        subscriber_len = 7
    elif len(area_code) == 3:
        # Major cities: area code "0XX", subscriber 6 digits
        subscriber_len = 6
    else:
        # Smaller cities: area code "0XXX", subscriber 5 digits
        subscriber_len = 5

    subscriber = "".join(str(rng.randint(0, 9)) for _ in range(subscriber_len))

    if international:
        return f"+359 {area_clean} {subscriber}"
    else:
        return f"0{area_clean} {subscriber}"
