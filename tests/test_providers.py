"""Tests for the BgTestData facade class."""

import allure

from bg_test_data.providers import BgTestData


@allure.epic("bg-test-data")
@allure.feature("BgTestData Facade")
class TestBgTestDataFacade:
    """Tests for the unified facade API."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Same seed produces identical output from the facade")
    def test_facade_seed_reproducibility(self) -> None:
        bg1 = BgTestData(seed=42)
        bg2 = BgTestData(seed=42)

        assert bg1.egn() == bg2.egn()
        # Fresh instances to compare person output
        bg3 = BgTestData(seed=123)
        bg4 = BgTestData(seed=123)
        p1 = bg3.person()
        p2 = bg4.person()
        assert p1["egn"] == p2["egn"]
        assert p1["first_name"] == p2["first_name"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("persons() returns the requested number of records")
    def test_batch_persons(self, bg: BgTestData) -> None:
        people = bg.persons(5)
        assert len(people) == 5
        for p in people:
            assert "egn" in p
            assert "first_name" in p

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("companies() returns the requested number of records")
    def test_batch_companies(self, bg: BgTestData) -> None:
        companies = bg.companies(3)
        assert len(companies) == 3
        for c in companies:
            assert "eik" in c
            assert "name" in c

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Static validate_egn works correctly")
    def test_static_validate_egn(self, bg: BgTestData) -> None:
        egn = bg.egn()
        assert BgTestData.validate_egn(egn) is True
        assert BgTestData.validate_egn("0000000000") is False

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Static validate_eik works correctly")
    def test_static_validate_eik(self, bg: BgTestData) -> None:
        eik = bg.eik()
        assert BgTestData.validate_eik(eik) is True
        assert BgTestData.validate_eik("12345678") is False

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Static validate_iban works correctly")
    def test_static_validate_iban(self, bg: BgTestData) -> None:
        iban = bg.iban()
        assert BgTestData.validate_iban(iban) is True
        assert BgTestData.validate_iban("BG00XXXX00000000000000") is False
