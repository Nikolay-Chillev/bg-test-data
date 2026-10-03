"""Tests for the Bulgarian address generator."""

import allure
import pytest

from bg_test_data._data.cities import CITIES
from bg_test_data._random import SeededRandom
from bg_test_data.address import generate_address, list_oblasts
from bg_test_data.providers import BgTestData


@allure.epic("bg-test-data")
@allure.feature("Address Generator")
class TestAddressGeneration:
    """Tests for Bulgarian address generation."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated address contains all required fields")
    def test_address_has_all_fields(self, rng: SeededRandom) -> None:
        address = generate_address(rng)
        expected_fields = {
            "street",
            "number",
            "city",
            "postal_code",
            "oblast",
            "oblast_code",
            "full_address",
        }
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


@allure.epic("bg-test-data")
@allure.feature("Address Generator")
@allure.story("ISO 3166-2 oblast codes")
class TestOblastCodes:
    """Tests for ISO 3166-2:BG oblast codes, used by e-commerce platforms to identify regions."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("All 28 oblasts have unique codes BG-01 to BG-28")
    def test_codes_cover_all_28_oblasts(self) -> None:
        codes = [oblast["code"] for oblast in list_oblasts()]
        assert codes == [f"BG-{n:02d}" for n in range(1, 29)]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Every city belongs to an oblast that has a code")
    def test_every_city_oblast_has_a_code(self) -> None:
        names = {oblast["name"] for oblast in list_oblasts()}
        missing = {oblast for _city, oblast, _postal, _area in CITIES} - names
        assert not missing, f"Oblasts without ISO code: {missing}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Generated address code matches its oblast")
    def test_address_code_matches_oblast(self, rng: SeededRandom) -> None:
        code_by_name = {oblast["name"]: oblast["code"] for oblast in list_oblasts()}
        for _ in range(50):
            address = generate_address(rng)
            assert address["oblast_code"] == code_by_name[address["oblast"]]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Specifying oblast_code returns address in that oblast")
    @pytest.mark.parametrize(
        ("code", "oblast_name"),
        [
            pytest.param("BG-22", "София-град", id="Sofia-City"),
            pytest.param("BG-23", "София", id="Sofia-Province"),
            pytest.param("BG-16", "Пловдив", id="Plovdiv"),
        ],
    )
    def test_address_with_oblast_code_parameter(
        self, rng: SeededRandom, code: str, oblast_name: str
    ) -> None:
        for _ in range(10):
            address = generate_address(rng, oblast_code=code)
            assert address["oblast_code"] == code
            assert address["oblast"] == oblast_name

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Unknown oblast code raises ValueError")
    @pytest.mark.parametrize("code", ["BG-29", "BG-00", "bg-22", "22", ""])
    def test_unknown_oblast_code_raises(self, rng: SeededRandom, code: str) -> None:
        with pytest.raises(ValueError, match="Oblast code not found"):
            generate_address(rng, oblast_code=code)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("oblast and oblast_code together raise ValueError")
    def test_oblast_and_oblast_code_are_exclusive(self, rng: SeededRandom) -> None:
        with pytest.raises(ValueError, match="either oblast or oblast_code"):
            generate_address(rng, oblast="Варна", oblast_code="BG-03")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Facade exposes the oblast list")
    def test_facade_lists_oblasts(self, bg: BgTestData) -> None:
        assert bg.oblasts() == list_oblasts()
