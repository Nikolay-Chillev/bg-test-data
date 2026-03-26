"""Tests for the Bulgarian company generator."""

import allure
import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.company import generate_company
from bg_test_data.egn import validate_egn
from bg_test_data.eik import validate_eik
from bg_test_data.iban import validate_iban


@allure.epic("bg-test-data")
@allure.feature("Company Generator")
class TestCompanyGeneration:
    """Tests for Bulgarian company data generation."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Generated company contains all required fields")
    def test_company_has_all_fields(self, rng: SeededRandom) -> None:
        company = generate_company(rng)
        expected_fields = {"name", "eik", "vat_number", "iban", "address", "phone", "manager"}
        assert expected_fields == set(company.keys())

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Company has a valid EIK")
    def test_company_has_valid_eik(self, rng: SeededRandom) -> None:
        for _ in range(20):
            company = generate_company(rng)
            assert validate_eik(str(company["eik"])), f"Invalid EIK: {company['eik']}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Company has a valid IBAN")
    def test_company_has_valid_iban(self, rng: SeededRandom) -> None:
        for _ in range(20):
            company = generate_company(rng)
            assert validate_iban(str(company["iban"])), f"Invalid IBAN: {company['iban']}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Company has a valid address with required fields")
    def test_company_has_address(self, rng: SeededRandom) -> None:
        company = generate_company(rng)
        address = company["address"]
        assert isinstance(address, dict)
        assert "city" in address
        assert "postal_code" in address

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Company manager is a valid person with valid EGN")
    def test_company_has_manager(self, rng: SeededRandom) -> None:
        company = generate_company(rng)
        manager = company["manager"]
        assert isinstance(manager, dict)
        assert "first_name" in manager
        assert "egn" in manager
        assert validate_egn(str(manager["egn"]))

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Company EIK length matches eik_length parameter")
    @pytest.mark.parametrize(
        "length",
        [pytest.param(9, id="eik-9"), pytest.param(13, id="eik-13")],
    )
    def test_company_eik_length_parameter(self, rng: SeededRandom, length: int) -> None:
        company = generate_company(rng, eik_length=length)
        assert len(str(company["eik"])) == length
        assert validate_eik(str(company["eik"]))

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Company VAT number is BG + EIK")
    def test_company_vat_number_format(self, rng: SeededRandom) -> None:
        company = generate_company(rng)
        assert str(company["vat_number"]).startswith("BG")
        assert str(company["vat_number"]) == f"BG{company['eik']}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Company name contains a legal form")
    def test_company_name_has_legal_form(self, rng: SeededRandom) -> None:
        legal_forms = [
            "\u0415\u041e\u041e\u0414",
            "\u041e\u041e\u0414",
            "\u0410\u0414",
            "\u0415\u0422",
            "\u0421\u0414",
            "\u041a\u0414",
            "\u041a\u0414\u0410",
        ]
        for _ in range(20):
            company = generate_company(rng)
            name = str(company["name"])
            assert any(lf in name for lf in legal_forms), (
                f"Company name '{name}' missing legal form"
            )
