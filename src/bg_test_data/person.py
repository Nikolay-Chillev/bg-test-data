"""Bulgarian person generator with correlated data."""

from datetime import date, timedelta

from bg_test_data._random import SeededRandom
from bg_test_data.address import generate_address
from bg_test_data.egn import Gender, generate_egn
from bg_test_data.names import generate_name
from bg_test_data.phone import generate_phone

# Cyrillic to Latin transliteration map for email generation
_TRANSLIT_MAP: dict[str, str] = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sht",
    "ъ": "a",
    "ь": "y",
    "ю": "yu",
    "я": "ya",
}

_EMAIL_DOMAINS = [
    "abv.bg",
    "mail.bg",
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "dir.bg",
]


def generate_person(
    rng: SeededRandom,
    *,
    gender: Gender | None = None,
    min_age: int = 18,
    max_age: int = 70,
) -> dict[str, object]:
    """Generate a complete Bulgarian person with correlated data.

    All generated data is internally consistent: name gender matches EGN gender,
    birth date matches EGN encoding, etc.

    Args:
        rng: Seeded random instance.
        gender: Force 'male' or 'female'. Random if None.
        min_age: Minimum age in years.
        max_age: Maximum age in years.

    Returns:
        Dict with first_name, middle_name, last_name, full_name, gender,
        birth_date (ISO string), egn, phone, email, address (dict).
    """
    if min_age > max_age:
        raise ValueError(f"min_age ({min_age}) must be <= max_age ({max_age})")
    if min_age < 0:
        raise ValueError(f"min_age must be >= 0, got {min_age}")

    if gender is None:
        gender = rng.choice(["male", "female"])

    # Generate a consistent birth date based on age range
    today = date.today()
    max_birth = date(today.year - min_age, today.month, today.day)
    min_birth = date(today.year - max_age - 1, today.month, today.day)

    # Pick a random day within the exact range
    total_days = (max_birth - min_birth).days
    if total_days <= 0:
        birth_date = min_birth
    else:
        random_days = rng.randint(0, total_days)
        birth_date = min_birth + timedelta(days=random_days)

    # Generate name matching gender
    name_data = generate_name(rng, gender=gender)

    # Generate EGN matching gender and birth date
    egn = generate_egn(rng, gender=gender, birth_date=birth_date)

    # Generate phone
    phone = generate_phone(rng)

    # Generate email from transliterated name
    email = _generate_email(rng, name_data["first_name"], name_data["last_name"])

    # Generate address
    address = generate_address(rng)

    return {
        "first_name": name_data["first_name"],
        "middle_name": name_data["middle_name"],
        "last_name": name_data["last_name"],
        "full_name": name_data["full_name"],
        "gender": gender,
        "birth_date": birth_date.isoformat(),
        "egn": egn,
        "phone": phone,
        "email": email,
        "address": address,
    }


def _transliterate(text: str) -> str:
    """Transliterate Cyrillic text to Latin characters."""
    result = []
    for char in text.lower():
        if char in _TRANSLIT_MAP:
            result.append(_TRANSLIT_MAP[char])
        elif char.isascii() and char.isalnum():
            result.append(char)
        # Skip non-translatable characters
    return "".join(result)


def _generate_email(rng: SeededRandom, first_name: str, last_name: str) -> str:
    """Generate an email address from transliterated Bulgarian names."""
    first = _transliterate(first_name)
    last = _transliterate(last_name)
    domain = rng.choice(_EMAIL_DOMAINS)

    # Choose a pattern
    pattern = rng.choice(["dot", "underscore", "first_only", "initial"])
    num_suffix = str(rng.randint(1, 99)) if rng.random() < 0.4 else ""

    if pattern == "dot":
        local = f"{first}.{last}{num_suffix}"
    elif pattern == "underscore":
        local = f"{first}_{last}{num_suffix}"
    elif pattern == "first_only":
        local = f"{first}{num_suffix}"
    else:  # initial
        local = f"{first[0]}.{last}{num_suffix}" if first and last else f"{first}{num_suffix}"

    return f"{local}@{domain}"
