"""Tests for the Bulgarian phone number generator."""

import re

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.phone import generate_phone


@allure.epic("bg-test-data")
@allure.feature("Phone Generator")
class TestPhoneGeneration:
    """Tests for phone number generation."""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Mobile number matches +359 8[789]X XXX XXXX pattern")
    def test_mobile_format(self, rng: SeededRandom) -> None:
        for _ in range(50):
            phone = generate_phone(rng, phone_type="mobile", international=True)
            assert re.match(r"^\+359 8[789] \d{3} \d{4}$", phone), (
                f"Mobile number '{phone}' does not match expected pattern"
            )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Landline number starts with +359 and has area code and subscriber digits")
    def test_landline_format(self, rng: SeededRandom) -> None:
        for _ in range(50):
            phone = generate_phone(rng, phone_type="landline", international=True)
            assert phone.startswith("+359 "), f"Landline '{phone}' missing +359 prefix"
            # After +359 there should be area code + subscriber
            rest = phone[5:]  # after "+359 "
            parts = rest.split(" ")
            assert len(parts) == 2, f"Landline '{phone}' expected area + subscriber"
            assert all(p.isdigit() for p in parts)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Local format phone starts with 0 instead of +359")
    @pytest.mark.parametrize("phone_type", ["mobile", "landline"])
    def test_local_format(self, rng: SeededRandom, phone_type: str) -> None:
        phone = generate_phone(rng, phone_type=phone_type, international=False)
        assert phone.startswith("0"), f"Local phone '{phone}' should start with 0"
        assert not phone.startswith("+359")
