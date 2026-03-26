"""Tests for the Bulgarian EGN (Unified Civil Number) generator and validator."""

from datetime import date

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.egn import generate_egn, parse_egn, validate_egn

_EGN_WEIGHTS = [2, 4, 8, 5, 10, 9, 7, 3, 6]


def _checksum_valid(egn: str) -> bool:
    """Independently verify EGN checksum."""
    digits = [int(d) for d in egn]
    total = sum(d * w for d, w in zip(digits[:9], _EGN_WEIGHTS, strict=False))
    remainder = total % 11
    expected = 0 if remainder == 10 else remainder
    return digits[9] == expected


@allure.epic("bg-test-data")
@allure.feature("EGN Generator")
class TestEgnGeneration:
    """Tests for EGN generation logic."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("EGN is exactly 10 characters long")
    def test_egn_length_10_digits(self, rng: SeededRandom) -> None:
        egn = generate_egn(rng)
        assert len(egn) == 10

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("EGN contains only digit characters")
    def test_egn_all_digits(self, rng: SeededRandom) -> None:
        egn = generate_egn(rng)
        assert egn.isdigit()

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("100 generated EGNs all have valid checksums")
    def test_egn_checksum_valid(self) -> None:
        rng = SeededRandom(seed=1)
        for _ in range(100):
            egn = generate_egn(rng)
            assert _checksum_valid(egn), f"Invalid checksum for EGN {egn}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Male EGN has even 9th digit")
    def test_egn_gender_male(self, rng: SeededRandom) -> None:
        for _ in range(50):
            egn = generate_egn(rng, gender="male")
            ninth_digit = int(egn[8])
            assert ninth_digit % 2 == 0, f"Male EGN {egn} has odd 9th digit {ninth_digit}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Female EGN has odd 9th digit")
    def test_egn_gender_female(self, rng: SeededRandom) -> None:
        for _ in range(50):
            egn = generate_egn(rng, gender="female")
            ninth_digit = int(egn[8])
            assert ninth_digit % 2 == 1, f"Female EGN {egn} has even 9th digit {ninth_digit}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("EGN with specific birth date round-trips through parse_egn")
    @pytest.mark.parametrize(
        "birth_date",
        [
            date(1985, 6, 15),
            date(1990, 1, 1),
            date(2001, 12, 31),
            date(1955, 3, 28),
        ],
        ids=["1985-06-15", "1990-01-01", "2001-12-31", "1955-03-28"],
    )
    def test_egn_specific_birth_date(self, rng: SeededRandom, birth_date: date) -> None:
        egn = generate_egn(rng, birth_date=birth_date)
        parsed = parse_egn(egn)
        assert parsed["birth_date"] == birth_date

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("1900s birth dates encode month as 1-12")
    @pytest.mark.parametrize("month", list(range(1, 13)))
    def test_egn_month_encoding_1900s(self, month: int) -> None:
        rng = SeededRandom(seed=month)
        bd = date(1980, month, 1)
        egn = generate_egn(rng, birth_date=bd)
        encoded_month = int(egn[2:4])
        assert encoded_month == month

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("2000s birth dates encode month as 41-52")
    @pytest.mark.parametrize("month", list(range(1, 13)))
    def test_egn_month_encoding_2000s(self, month: int) -> None:
        rng = SeededRandom(seed=month)
        bd = date(2003, month, 15)
        egn = generate_egn(rng, birth_date=bd)
        encoded_month = int(egn[2:4])
        assert encoded_month == month + 40

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Same seed produces identical EGN sequence")
    def test_egn_seed_reproducibility(self) -> None:
        rng1 = SeededRandom(seed=42)
        rng2 = SeededRandom(seed=42)
        egns1 = [generate_egn(rng1) for _ in range(10)]
        egns2 = [generate_egn(rng2) for _ in range(10)]
        assert egns1 == egns2


@allure.epic("bg-test-data")
@allure.feature("EGN Validator")
class TestEgnValidation:
    """Tests for EGN validation."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Known valid EGN passes validation")
    def test_validate_egn_known_valid(self, rng: SeededRandom) -> None:
        egn = generate_egn(rng)
        assert validate_egn(egn) is True

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Manually constructed EGNs with hand-calculated checksums pass validation")
    @pytest.mark.parametrize(
        "egn,expected_gender,expected_year",
        [
            pytest.param("8506150000", "male", 1985, id="1985-male-region0"),
            pytest.param("0141015034", "female", 2001, id="2001-female-month41"),
        ],
    )
    def test_validate_egn_manually_constructed(
        self, egn: str, expected_gender: str, expected_year: int
    ) -> None:
        """Verify against hand-calculated EGNs (independent of generator)."""
        assert validate_egn(egn) is True
        parsed = parse_egn(egn)
        assert parsed["gender"] == expected_gender
        assert parsed["birth_date"].year == expected_year  # type: ignore[union-attr]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("EGN with tampered checksum fails validation")
    def test_validate_egn_invalid_checksum(self, rng: SeededRandom) -> None:
        egn = generate_egn(rng)
        # Flip the last digit
        bad_digit = (int(egn[9]) + 1) % 10
        bad_egn = egn[:9] + str(bad_digit)
        assert validate_egn(bad_egn) is False

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("EGN with wrong length fails validation")
    @pytest.mark.parametrize("value", ["123456789", "12345678901", ""])
    def test_validate_egn_invalid_length(self, value: str) -> None:
        assert validate_egn(value) is False

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("EGN with non-digit characters fails validation")
    @pytest.mark.parametrize("value", ["123456789a", "abcdefghij", "12345 6789"])
    def test_validate_egn_non_digits(self, value: str) -> None:
        assert validate_egn(value) is False


@allure.epic("bg-test-data")
@allure.feature("EGN Parser")
class TestEgnParser:
    """Tests for EGN parsing and error handling."""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("parse_egn raises ValueError for invalid input")
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("12345", id="too-short"),
            pytest.param("abcdefghij", id="non-digits"),
            pytest.param("", id="empty-string"),
        ],
    )
    def test_parse_egn_raises_value_error(self, value: str) -> None:
        with pytest.raises(ValueError, match="EGN must be exactly 10 digits"):
            parse_egn(value)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("generate_egn raises ValueError for unsupported year")
    def test_generate_egn_invalid_year_range(self, rng: SeededRandom) -> None:
        with pytest.raises(ValueError, match="out of supported range"):
            generate_egn(rng, birth_date=date(2100, 1, 1))

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("parse_egn round-trips with generated EGN")
    def test_parse_egn_round_trip(self) -> None:
        rng = SeededRandom(seed=99)
        for _ in range(50):
            gender = rng.choice(["male", "female"])
            egn = generate_egn(rng, gender=gender)
            parsed = parse_egn(egn)
            assert parsed["gender"] == gender
            assert isinstance(parsed["birth_date"], date)
            assert isinstance(parsed["region"], int)
