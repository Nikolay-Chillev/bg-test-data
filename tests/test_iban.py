"""Tests for the Bulgarian IBAN generator and validator."""

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.iban import format_iban, generate_iban, validate_iban


@allure.epic("bg-test-data")
@allure.feature("IBAN Generator")
class TestIbanGeneration:
    """Tests for IBAN generation, validation, and formatting."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated IBAN is exactly 22 characters long")
    def test_iban_length_22(self, rng: SeededRandom) -> None:
        iban = generate_iban(rng)
        assert len(iban) == 22

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated IBAN starts with 'BG'")
    def test_iban_starts_with_bg(self, rng: SeededRandom) -> None:
        iban = generate_iban(rng)
        assert iban.startswith("BG")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("100 generated IBANs all pass mod-97 validation")
    def test_iban_mod97_valid(self) -> None:
        rng = SeededRandom(seed=1)
        for _ in range(100):
            iban = generate_iban(rng)
            assert validate_iban(iban), f"Invalid IBAN: {iban}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("IBAN generated with a specific bank code contains that code")
    @pytest.mark.parametrize("bank_code", ["UNCR", "BNBG", "STSA"])
    def test_iban_specific_bank_code(self, rng: SeededRandom, bank_code: str) -> None:
        iban = generate_iban(rng, bank_code=bank_code)
        assert iban[4:8] == bank_code

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Invalid IBAN strings fail validation")
    @pytest.mark.parametrize(
        "value",
        [
            "BG00UNCR12345678901234",  # likely bad check digits
            "DE89370400440532013000",  # wrong country
            "BG12UNCR",  # too short
            "",  # empty
            "BGXXUNCR12345678901234",  # non-digit check digits
        ],
        ids=["bad-check", "wrong-country", "too-short", "empty", "non-digit-check"],
    )
    def test_validate_iban_invalid(self, value: str) -> None:
        assert validate_iban(value) is False

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("format_iban splits IBAN into groups of 4 separated by spaces")
    def test_format_iban(self, rng: SeededRandom) -> None:
        iban = generate_iban(rng)
        formatted = format_iban(iban)
        parts = formatted.split(" ")
        # 22 chars -> groups of 4,4,4,4,4,2
        assert all(len(p) == 4 for p in parts[:-1])
        assert 1 <= len(parts[-1]) <= 4
        assert formatted.replace(" ", "") == iban

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Invalid bank_code raises ValueError")
    @pytest.mark.parametrize(
        "code",
        [
            pytest.param("AB", id="too-short"),
            pytest.param("ABCDE", id="too-long"),
            pytest.param("12AB", id="contains-digits"),
        ],
    )
    def test_invalid_bank_code_raises(self, rng: SeededRandom, code: str) -> None:
        with pytest.raises(ValueError, match="bank_code must be exactly 4 letters"):
            generate_iban(rng, bank_code=code)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Formatted IBAN with spaces passes validation")
    def test_validate_iban_with_spaces(self, rng: SeededRandom) -> None:
        iban = generate_iban(rng)
        formatted = format_iban(iban)
        assert " " in formatted
        assert validate_iban(formatted) is True

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Manually constructed EIK-9 with hand-calculated checksum passes validation")
    def test_known_valid_eik(self) -> None:
        """EIK 123456786: weights [1,2,3,4,5,6,7,8] on 12345678, sum=204, mod11=6."""
        from bg_test_data.eik import validate_eik

        assert validate_eik("123456786") is True
        assert validate_eik("123456780") is False  # wrong check digit
