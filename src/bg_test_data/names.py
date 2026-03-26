"""Bulgarian name generator with gender-aware patronymic rules."""

from bg_test_data._data.first_names_female import FEMALE_FIRST_NAMES
from bg_test_data._data.first_names_male import MALE_FIRST_NAMES
from bg_test_data._data.last_names import LAST_NAME_BASES
from bg_test_data._random import SeededRandom
from bg_test_data.egn import Gender

# Cyrillic vowels (used for patronymic suffix rules)
_VOWELS = set("аеиоуъюяАЕИОУЪЮЯ")
# Soft consonants that take -ев/-ева instead of -ов/-ова
_SOFT_CONSONANTS = set("йЙьЬ")


def generate_name(
    rng: SeededRandom,
    *,
    gender: Gender | None = None,
) -> dict[str, str]:
    """Generate a Bulgarian full name with patronymic middle name.

    Args:
        rng: Seeded random instance.
        gender: Force 'male' or 'female'. Random if None.

    Returns:
        Dict with first_name, middle_name, last_name, full_name, gender.
    """
    if gender is None:
        gender = rng.choice(["male", "female"])

    # Pick first name based on gender
    if gender == "male":
        first_name = rng.choice(MALE_FIRST_NAMES)
    else:
        first_name = rng.choice(FEMALE_FIRST_NAMES)

    # Pick a father's first name (always male) for the patronymic middle name
    father_name = rng.choice(MALE_FIRST_NAMES)
    middle_name = _make_patronymic(father_name, gender)

    # Pick a last name base and adjust for gender
    last_name_base = rng.choice(LAST_NAME_BASES)
    last_name = _adjust_last_name(last_name_base, gender)

    full_name = f"{first_name} {middle_name} {last_name}"

    return {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "full_name": full_name,
        "gender": gender,
    }


def _make_patronymic(father_name: str, gender: Gender) -> str:
    """Create a patronymic (middle name) from a father's first name.

    Rules:
    - If father's name ends in a vowel, drop it and add -ов/-ова (male/female)
    - If father's name ends in a soft consonant (й, ь), drop it and add -ев/-ева
    - Otherwise (hard consonant), add -ов/-ова
    """
    name = father_name.rstrip()

    if not name:
        return name

    last_char = name[-1]

    if last_char in _VOWELS:
        # Drop the vowel and add suffix
        base = name[:-1]
        # After dropping a vowel, check the new last char
        if base and base[-1] in _SOFT_CONSONANTS:
            base = base[:-1]
            suffix = "ев" if gender == "male" else "ева"
        else:
            suffix = "ов" if gender == "male" else "ова"
    elif last_char in _SOFT_CONSONANTS:
        # Drop the soft consonant and add -ев/-ева
        base = name[:-1]
        suffix = "ев" if gender == "male" else "ева"
    elif last_char == "р" or last_char == "л":
        # р and л typically get -ов/-ова
        base = name
        suffix = "ов" if gender == "male" else "ова"
    else:
        # Hard consonant - add -ов/-ова
        base = name
        suffix = "ов" if gender == "male" else "ова"

    return base + suffix


def _adjust_last_name(last_name_base: str, gender: Gender) -> str:
    """Adjust a masculine last name base for the given gender.

    Masculine names end in -ов or -ев.
    Female forms add -а: -ов -> -ова, -ев -> -ева.
    """
    if gender == "male":
        return last_name_base

    # Female: add -а to the masculine form
    if last_name_base.endswith("ов") or last_name_base.endswith("ев"):
        return last_name_base + "а"
    elif last_name_base.endswith("ски"):
        return last_name_base[:-1] + "а"
    else:
        return last_name_base + "а"
