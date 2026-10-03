"""Bulgarian address generator."""

from bg_test_data._data.cities import CITIES
from bg_test_data._data.oblasts import OBLAST_CODES
from bg_test_data._data.streets import DEFAULT_STREETS, STREETS
from bg_test_data._random import SeededRandom


def generate_address(
    rng: SeededRandom,
    *,
    city: str | None = None,
    oblast: str | None = None,
    oblast_code: str | None = None,
) -> dict[str, str]:
    """Generate a Bulgarian postal address.

    Args:
        rng: Seeded random instance.
        city: Specific city name. Random if None.
        oblast: Filter cities by oblast name. Ignored if city is specified.
        oblast_code: Filter cities by ISO 3166-2 oblast code, e.g. "BG-22".
            Ignored if city is specified; cannot be combined with oblast.

    Returns:
        Dict with street, number, city, postal_code, oblast, oblast_code, full_address.
    """
    if oblast_code is not None:
        if oblast is not None:
            raise ValueError("Pass either oblast or oblast_code, not both")
        oblast = _oblast_name(oblast_code)

    # Select city
    city_data = _select_city(rng, city=city, oblast=oblast)

    city_name, oblast_name, postal_code, _area_code = city_data

    # Select street
    city_streets = STREETS.get(city_name, DEFAULT_STREETS)
    street_name = rng.choice(city_streets)

    # Generate building number (typical Bulgarian range: 1-150)
    number = str(rng.randint(1, 150))

    # 30% chance to add apartment details (simulating block housing)
    extra = ""
    if rng.random() < 0.3:
        entrance = rng.choice(["А", "Б", "В", "Г"])
        floor = rng.randint(1, 12)
        apt = rng.randint(1, 60)
        extra = f", вх. {entrance}, ет. {floor}, ап. {apt}"

    full_address = f"ул. {street_name} {number}{extra}, {postal_code} {city_name}"

    return {
        "street": street_name,
        "number": number,
        "city": city_name,
        "postal_code": postal_code,
        "oblast": oblast_name,
        "oblast_code": OBLAST_CODES[oblast_name],
        "full_address": full_address,
    }


def list_oblasts() -> list[dict[str, str]]:
    """Return all 28 oblasts as dicts with name and ISO 3166-2 code, ordered by code."""
    return [
        {"name": name, "code": code}
        for name, code in sorted(OBLAST_CODES.items(), key=lambda item: item[1])
    ]


def _oblast_name(oblast_code: str) -> str:
    """Return the oblast name for an ISO 3166-2 code.

    Raises:
        ValueError: If the code is not a Bulgarian oblast code.
    """
    for name, code in OBLAST_CODES.items():
        if code == oblast_code:
            return name
    raise ValueError(f"Oblast code not found: {oblast_code!r}")


def _select_city(
    rng: SeededRandom,
    *,
    city: str | None = None,
    oblast: str | None = None,
) -> tuple[str, str, str, str]:
    """Select a city from the CITIES list, filtering by city or oblast.

    Raises:
        ValueError: If the specified city or oblast is not found.
    """
    if city is not None:
        matching = [c for c in CITIES if c[0] == city]
        if not matching:
            raise ValueError(f"City not found: {city!r}")
        return rng.choice(matching)

    if oblast is not None:
        matching = [c for c in CITIES if c[1] == oblast]
        if not matching:
            raise ValueError(f"Oblast not found: {oblast!r}")
        return rng.choice(matching)

    return rng.choice(CITIES)
