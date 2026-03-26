"""BgTestData facade class providing a unified API for all generators."""

from typing import Any

from bg_test_data._random import SeededRandom
from bg_test_data.address import generate_address
from bg_test_data.company import generate_company
from bg_test_data.egn import generate_egn, parse_egn, validate_egn
from bg_test_data.eik import generate_eik, validate_eik
from bg_test_data.iban import generate_iban, validate_iban
from bg_test_data.names import generate_name
from bg_test_data.person import generate_person
from bg_test_data.phone import generate_phone


class BgTestData:
    """Facade for generating Bulgarian test data.

    All data is reproducible when a seed is provided.

    Usage::

        bg = BgTestData(seed=42)
        person = bg.person()
        company = bg.company()
    """

    def __init__(self, seed: int | None = None) -> None:
        self._rng = SeededRandom(seed)

    # --- Single-record generators ---

    def egn(self, **kwargs: Any) -> str:
        """Generate a valid Bulgarian EGN. Options: gender."""
        return generate_egn(self._rng, **kwargs)

    def eik(self, **kwargs: Any) -> str:
        """Generate a valid Bulgarian EIK/BULSTAT. Options: length (9 or 13)."""
        return generate_eik(self._rng, **kwargs)

    def iban(self, **kwargs: Any) -> str:
        """Generate a valid Bulgarian IBAN. Options: bank_code."""
        return generate_iban(self._rng, **kwargs)

    def phone(self, **kwargs: Any) -> str:
        """Generate a Bulgarian phone number. Options: phone_type, international."""
        return generate_phone(self._rng, **kwargs)

    def name(self, **kwargs: Any) -> dict[str, str]:
        """Generate a Bulgarian name. Options: gender."""
        return generate_name(self._rng, **kwargs)

    def address(self, **kwargs: Any) -> dict[str, str]:
        """Generate a Bulgarian address. Options: city, oblast."""
        return generate_address(self._rng, **kwargs)

    def person(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a complete Bulgarian person. Options: gender, min_age, max_age."""
        return generate_person(self._rng, **kwargs)

    def company(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a Bulgarian company. Options: eik_length."""
        return generate_company(self._rng, **kwargs)

    # --- Batch generators ---

    def persons(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        """Generate multiple Bulgarian persons."""
        return [self.person(**kwargs) for _ in range(count)]

    def companies(self, count: int, **kwargs: Any) -> list[dict[str, Any]]:
        """Generate multiple Bulgarian companies."""
        return [self.company(**kwargs) for _ in range(count)]

    # --- Validators (static) ---

    @staticmethod
    def validate_egn(egn: str) -> bool:
        """Validate a Bulgarian EGN checksum."""
        return validate_egn(egn)

    @staticmethod
    def validate_eik(eik: str) -> bool:
        """Validate a Bulgarian EIK/BULSTAT checksum."""
        return validate_eik(eik)

    @staticmethod
    def validate_iban(iban: str) -> bool:
        """Validate a Bulgarian IBAN (mod-97 check)."""
        return validate_iban(iban)

    @staticmethod
    def parse_egn(egn: str) -> dict[str, object]:
        """Parse an EGN and extract birth date, gender, and region."""
        return parse_egn(egn)
