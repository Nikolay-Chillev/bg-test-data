"""Tests for the Bulgarian name generator."""

import allure

from bg_test_data._random import SeededRandom
from bg_test_data.names import generate_name


@allure.epic("bg-test-data")
@allure.feature("Name Generator")
class TestNameGeneration:
    """Tests for Bulgarian name generation with patronymic rules."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated name contains all required fields")
    def test_name_has_all_fields(self, rng: SeededRandom) -> None:
        name = generate_name(rng)
        expected_fields = {"first_name", "middle_name", "last_name", "full_name", "gender"}
        assert expected_fields == set(name.keys())
        for field in expected_fields:
            assert isinstance(name[field], str)
            assert len(name[field]) > 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Male name has masculine last name ending (-ов, -ев, -ски)")
    def test_male_name(self, rng: SeededRandom) -> None:
        for _ in range(50):
            name = generate_name(rng, gender="male")
            assert name["gender"] == "male"
            last = name["last_name"]
            assert last.endswith("ов") or last.endswith("ев") or last.endswith("ски"), (
                f"Male last name '{last}' does not end with expected suffix"
            )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Female name has feminine last name ending (-ова, -ева, -ска)")
    def test_female_name(self, rng: SeededRandom) -> None:
        for _ in range(50):
            name = generate_name(rng, gender="female")
            assert name["gender"] == "female"
            last = name["last_name"]
            assert (
                last.endswith("ова")
                or last.endswith("ева")
                or last.endswith("ска")
                or last.endswith("а")
            ), f"Female last name '{last}' does not end with expected feminine suffix"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Full name consists of exactly three parts")
    def test_full_name_three_parts(self, rng: SeededRandom) -> None:
        name = generate_name(rng)
        parts = name["full_name"].split()
        assert len(parts) == 3

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Name without gender specified still returns valid gender")
    def test_gender_random(self, rng: SeededRandom) -> None:
        name = generate_name(rng)
        assert name["gender"] in ("male", "female")
