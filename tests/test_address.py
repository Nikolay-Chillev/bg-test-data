"""Tests for the Bulgarian address generator."""

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.address import generate_address


@allure.epic("bg-test-data")
@allure.feature("Address Generator")
class TestAddressGeneration:
    """Tests for Bulgarian address generation."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated address contains all required fields")
    def test_address_has_all_fields(self, rng: SeededRandom) -> None:
        address = generate_address(rng)
        expected_fields = {"street", "number", "city", "postal_code", "oblast", "full_address"}
        assert expected_fields == set(address.keys())
        for field in expected_fields:
            assert isinstance(address[field], str)
            assert len(address[field]) > 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Postal code is exactly 4 digits")
    def test_postal_code_4_digits(self, rng: SeededRandom) -> None:
        for _ in range(50):
            address = generate_address(rng)
            pc = address["postal_code"]
            assert len(pc) == 4, f"Postal code '{pc}' is not 4 characters"
            assert pc.isdigit(), f"Postal code '{pc}' contains non-digit characters"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Full address string contains the city name")
    def test_full_address_contains_city(self, rng: SeededRandom) -> None:
        for _ in range(30):
            address = generate_address(rng)
            assert address["city"] in address["full_address"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Specifying city returns address in that city")
    @pytest.mark.parametrize(
        "city_name",
        [
            pytest.param("\u0421\u043e\u0444\u0438\u044f", id="Sofia"),
            pytest.param("\u041f\u043b\u043e\u0432\u0434\u0438\u0432", id="Plovdiv"),
            pytest.param("\u0412\u0430\u0440\u043d\u0430", id="Varna"),
        ],
    )
    def test_address_with_city_parameter(self, rng: SeededRandom, city_name: str) -> None:
        address = generate_address(rng, city=city_name)
        assert address["city"] == city_name

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Specifying oblast returns address in that oblast")
    def test_address_with_oblast_parameter(self, rng: SeededRandom) -> None:
        for _ in range(10):
            address = generate_address(rng, oblast="\u041f\u043b\u043e\u0432\u0434\u0438\u0432")
            assert address["oblast"] == "\u041f\u043b\u043e\u0432\u0434\u0438\u0432"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Unknown city raises ValueError")
    def test_unknown_city_raises(self, rng: SeededRandom) -> None:
        with pytest.raises(ValueError, match="City not found"):
            generate_address(rng, city="FakeCity")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Unknown oblast raises ValueError")
    def test_unknown_oblast_raises(self, rng: SeededRandom) -> None:
        with pytest.raises(ValueError, match="Oblast not found"):
            generate_address(rng, oblast="FakeOblast")
