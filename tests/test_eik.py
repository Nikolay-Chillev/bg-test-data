"""Tests for the Bulgarian EIK/BULSTAT generator and validator."""

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.eik import generate_eik, validate_eik


@allure.epic("bg-test-data")
@allure.feature("EIK Generator")
class TestEikGeneration:
    """Tests for EIK generation and validation."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("9-digit EIK has exactly 9 characters")
    def test_eik9_length(self, rng: SeededRandom) -> None:
        eik = generate_eik(rng, length=9)
        assert len(eik) == 9

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("100 generated 9-digit EIKs all pass validation")
    def test_eik9_valid_checksum(self) -> None:
        rng = SeededRandom(seed=1)
        for _ in range(100):
            eik = generate_eik(rng, length=9)
            assert validate_eik(eik), f"Invalid EIK-9: {eik}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("13-digit EIK has exactly 13 characters")
    def test_eik13_length(self, rng: SeededRandom) -> None:
        eik = generate_eik(rng, length=13)
        assert len(eik) == 13

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("100 generated 13-digit EIKs all pass validation")
    def test_eik13_valid_checksum(self) -> None:
        rng = SeededRandom(seed=1)
        for _ in range(100):
            eik = generate_eik(rng, length=13)
            assert validate_eik(eik), f"Invalid EIK-13: {eik}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Invalid EIK strings fail validation")
    @pytest.mark.parametrize(
        "value",
        [
            "12345678",  # too short
            "1234567890",  # 10 digits (invalid length)
            "12345678901234",  # too long
            "abcdefghi",  # letters
            "",  # empty
            "00000000X",  # non-digit character
        ],
        ids=["8-digits", "10-digits", "14-digits", "letters", "empty", "non-digit"],
    )
    def test_validate_eik_invalid(self, value: str) -> None:
        assert validate_eik(value) is False

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Generated EIK contains only digit characters")
    @pytest.mark.parametrize("length", [9, 13], ids=["eik9", "eik13"])
    def test_eik_all_digits(self, rng: SeededRandom, length: int) -> None:
        eik = generate_eik(rng, length=length)
        assert eik.isdigit()
