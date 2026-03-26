"""Tests for the Bulgarian person generator."""

from datetime import date
from typing import Any

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.egn import parse_egn, validate_egn
from bg_test_data.person import generate_person


@allure.epic("bg-test-data")
@allure.feature("Person Generator")
class TestPersonGeneration:
    """Tests for correlated person data generation."""

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated person contains all required fields")
    def test_person_has_all_fields(self, rng: SeededRandom) -> None:
        person = generate_person(rng)
        expected_fields = {
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "gender",
            "birth_date",
            "egn",
            "phone",
            "email",
            "address",
        }
        assert expected_fields == set(person.keys())

    @pytest.mark.integration
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Person EGN gender matches the name gender")
    @pytest.mark.parametrize(
        "gender",
        [
            pytest.param("male", id="male-correlation"),
            pytest.param("female", id="female-correlation"),
        ],
    )
    def test_person_gender_correlation(self, rng: SeededRandom, gender: str) -> None:
        for _ in range(30):
            person = generate_person(rng, gender=gender)
            parsed = parse_egn(str(person["egn"]))
            assert parsed["gender"] == gender

    @pytest.mark.integration
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Person birth_date matches the date encoded in the EGN")
    def test_person_birth_date_in_egn(self, rng: SeededRandom) -> None:
        for _ in range(30):
            person = generate_person(rng)
            parsed = parse_egn(str(person["egn"]))
            assert parsed["birth_date"] == date.fromisoformat(str(person["birth_date"]))

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Person has a valid EGN")
    def test_person_has_valid_egn(self, rng: SeededRandom) -> None:
        for _ in range(30):
            person = generate_person(rng)
            assert validate_egn(str(person["egn"])), f"Invalid EGN: {person['egn']}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Person has a valid email format")
    def test_person_has_email(self, rng: SeededRandom) -> None:
        person = generate_person(rng)
        email = str(person["email"])
        assert "@" in email
        assert "." in email.split("@")[1]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Person age is within the requested range")
    @pytest.mark.parametrize(
        "min_age,max_age",
        [
            pytest.param(18, 30, id="young-adults"),
            pytest.param(40, 60, id="middle-aged"),
            pytest.param(25, 25, id="exact-age"),
        ],
    )
    def test_person_age_range(self, min_age: int, max_age: int) -> None:
        rng = SeededRandom(seed=10)
        for _ in range(20):
            person = generate_person(rng, min_age=min_age, max_age=max_age)
            birth = date.fromisoformat(str(person["birth_date"]))
            today = date.today()
            # Exact age calculation accounting for birthday this year
            had_birthday = (today.month, today.day) >= (birth.month, birth.day)
            age = today.year - birth.year - (0 if had_birthday else 1)
            assert min_age <= age <= max_age, (
                f"Age {age} outside expected range [{min_age}-{max_age}]"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Person address is a dict with required fields")
    def test_person_address_structure(self, rng: SeededRandom) -> None:
        person = generate_person(rng)
        address = person["address"]
        assert isinstance(address, dict)
        assert "city" in address
        assert "street" in address
        assert "postal_code" in address

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Factory fixture produces valid persons")
    def test_factory_fixture(self, make_person: Any) -> None:
        male = make_person(gender="male")
        female = make_person(gender="female")
        assert male["gender"] == "male"
        assert female["gender"] == "female"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("min_age > max_age raises ValueError")
    def test_person_invalid_age_range(self, rng: SeededRandom) -> None:
        with pytest.raises(ValueError, match="min_age.*must be <= max_age"):
            generate_person(rng, min_age=50, max_age=20)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Negative min_age raises ValueError")
    def test_person_negative_age(self, rng: SeededRandom) -> None:
        with pytest.raises(ValueError, match="min_age must be >= 0"):
            generate_person(rng, min_age=-5)
