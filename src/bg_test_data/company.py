"""Bulgarian company generator."""

from bg_test_data._random import SeededRandom
from bg_test_data.address import generate_address
from bg_test_data.eik import EikLength, generate_eik
from bg_test_data.iban import generate_iban
from bg_test_data.person import generate_person
from bg_test_data.phone import generate_phone

_LEGAL_FORMS = ["ЕООД", "ООД", "АД", "ЕТ", "СД", "КД"]

_ADJECTIVES = [
    "Балканска",
    "Българска",
    "Велика",
    "Глобална",
    "Добра",
    "Европейска",
    "Златна",
    "Интер",
    "Модерна",
    "Нова",
    "Обединена",
    "Първа",
    "Родна",
    "Стара",
    "Тракийска",
    "Успешна",
    "Черноморска",
    "Южна",
    "Столична",
    "Национална",
]

_NOUNS = [
    "Агро",
    "Билд",
    "Визия",
    "Груп",
    "Дизайн",
    "Експрес",
    "Инвест",
    "Камък",
    "Комерс",
    "Консулт",
    "Креатив",
    "Логистик",
    "Маркет",
    "Партнърс",
    "Плюс",
    "Прогрес",
    "Ресурс",
    "Системи",
    "Строй",
    "Тех",
    "Търговия",
    "Услуги",
    "Финанс",
    "Холдинг",
    "Център",
    "Електроникс",
    "Индустрия",
    "Енерджи",
    "Транс",
    "Мениджмънт",
]


def generate_company(
    rng: SeededRandom,
    *,
    eik_length: EikLength = 9,
    legal_form: str | None = None,
) -> dict[str, object]:
    """Generate a Bulgarian company with correlated data.

    Args:
        rng: Seeded random instance.
        eik_length: 9 or 13 digit EIK.
        legal_form: Specific legal form (e.g. 'ЕООД'). Random if None.

    Returns:
        Dict with name, eik, vat_number, iban, address, phone, manager.
    """
    if legal_form is None:
        legal_form = rng.choice(_LEGAL_FORMS)

    # Generate company name
    name = _generate_company_name(rng, legal_form)

    # Generate EIK
    eik = generate_eik(rng, length=eik_length)

    # VAT number = BG + EIK
    vat_number = f"BG{eik}"

    # Generate IBAN
    iban = generate_iban(rng)

    # Generate address
    address = generate_address(rng)

    # Generate phone
    phone = generate_phone(rng, phone_type="landline")

    # Generate manager (a person)
    manager = generate_person(rng, min_age=25, max_age=65)

    return {
        "name": name,
        "eik": eik,
        "vat_number": vat_number,
        "iban": iban,
        "address": address,
        "phone": phone,
        "manager": manager,
    }


def _generate_company_name(rng: SeededRandom, legal_form: str) -> str:
    """Generate a Bulgarian-style company name."""
    pattern = rng.choice(["adj_noun", "noun_only", "double_noun"])

    if pattern == "adj_noun":
        adj = rng.choice(_ADJECTIVES)
        noun = rng.choice(_NOUNS)
        base = f"{adj} {noun}"
    elif pattern == "noun_only":
        noun = rng.choice(_NOUNS)
        base = noun
    else:  # double_noun
        noun1 = rng.choice(_NOUNS)
        noun2 = rng.choice(_NOUNS)
        while noun2 == noun1:
            noun2 = rng.choice(_NOUNS)
        base = f"{noun1} {noun2}"

    return f"{base} {legal_form}"
