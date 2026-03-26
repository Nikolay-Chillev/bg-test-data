"""Tests for the bg-test-data command-line interface."""

import json
from io import StringIO
from unittest.mock import patch

import allure
import pytest

from bg_test_data.cli import main


@allure.epic("bg-test-data")
@allure.feature("CLI")
class TestCli:
    """Tests for the CLI entry point."""

    @staticmethod
    def _run(argv: list[str]) -> str:
        """Run main() with given argv and capture stdout."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main(argv)
        return mock_stdout.getvalue().strip()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("CLI 'person' command outputs valid JSON")
    def test_cli_person(self) -> None:
        output = self._run(["--seed", "42", "person"])
        data = json.loads(output)
        assert "egn" in data
        assert "first_name" in data
        assert "gender" in data

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("CLI 'egn' command outputs valid EGN")
    def test_cli_egn(self) -> None:
        output = self._run(["--seed", "42", "egn"])
        data = json.loads(output)
        assert "value" in data
        assert len(data["value"]) == 10
        assert data["value"].isdigit()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("CLI 'eik' command outputs valid EIK")
    def test_cli_eik(self) -> None:
        output = self._run(["--seed", "42", "eik"])
        data = json.loads(output)
        assert "value" in data
        assert len(data["value"]) == 9

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'eik' with --length 13")
    def test_cli_eik_13(self) -> None:
        output = self._run(["--seed", "42", "eik", "--length", "13"])
        data = json.loads(output)
        assert len(data["value"]) == 13

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("CLI 'iban' command outputs valid IBAN")
    def test_cli_iban(self) -> None:
        output = self._run(["--seed", "42", "iban"])
        data = json.loads(output)
        assert "value" in data
        assert data["value"].startswith("BG")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'phone' command outputs phone number")
    def test_cli_phone(self) -> None:
        output = self._run(["--seed", "42", "phone"])
        data = json.loads(output)
        assert "value" in data

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'phone' with --type mobile")
    def test_cli_phone_mobile(self) -> None:
        output = self._run(["--seed", "42", "phone", "--type", "mobile"])
        data = json.loads(output)
        assert "+359" in data["value"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'name' command outputs name dict")
    def test_cli_name(self) -> None:
        output = self._run(["--seed", "42", "name"])
        data = json.loads(output)
        assert "first_name" in data
        assert "last_name" in data

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'name' with --gender male")
    def test_cli_name_gender(self) -> None:
        output = self._run(["--seed", "42", "name", "--gender", "male"])
        data = json.loads(output)
        assert data["gender"] == "male"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'address' command outputs address dict")
    def test_cli_address(self) -> None:
        output = self._run(["--seed", "42", "address"])
        data = json.loads(output)
        assert "city" in data
        assert "street" in data

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'company' command outputs company dict")
    def test_cli_company(self) -> None:
        output = self._run(["--seed", "42", "company"])
        data = json.loads(output)
        assert "eik" in data
        assert "name" in data

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'company' with --eik-length 13")
    def test_cli_company_eik13(self) -> None:
        output = self._run(["--seed", "42", "company", "--eik-length", "13"])
        data = json.loads(output)
        assert len(data["eik"]) == 13

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("CLI --count flag generates the requested number of records")
    @pytest.mark.parametrize("count", [1, 3, 5])
    def test_cli_count(self, count: int) -> None:
        output = self._run(["--seed", "1", "--count", str(count), "person"])
        data = json.loads(output)
        if count == 1:
            assert isinstance(data, dict)
        else:
            assert isinstance(data, list)
            assert len(data) == count

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI --count with string type (egn)")
    def test_cli_count_string_type(self) -> None:
        output = self._run(["--seed", "1", "--count", "3", "egn"])
        data = json.loads(output)
        assert isinstance(data, list)
        assert len(data) == 3

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("CLI with same seed produces identical output")
    def test_cli_seed_reproducible(self) -> None:
        output1 = self._run(["--seed", "99", "egn"])
        output2 = self._run(["--seed", "99", "egn"])
        assert output1 == output2

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI with no command shows help and exits")
    def test_cli_no_command(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            self._run([])
        assert exc_info.value.code == 1

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI --format csv for person")
    def test_cli_csv_format_person(self) -> None:
        output = self._run(["--seed", "42", "--format", "csv", "person"])
        assert "," in output  # CSV has commas
        lines = output.strip().split("\n")
        assert len(lines) >= 2  # header + data

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI --format csv for string type")
    def test_cli_csv_format_string(self) -> None:
        output = self._run(["--seed", "42", "--format", "csv", "egn"])
        assert len(output) == 10  # raw EGN, no JSON wrapper

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI --format csv with --count for string type")
    def test_cli_csv_format_string_count(self) -> None:
        output = self._run(["--seed", "42", "--format", "csv", "--count", "3", "egn"])
        lines = output.strip().split("\n")
        assert len(lines) == 3

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI --format csv with --count for dict type")
    def test_cli_csv_format_dict_count(self) -> None:
        output = self._run(["--seed", "42", "--format", "csv", "--count", "2", "person"])
        lines = output.strip().split("\n")
        assert len(lines) >= 3  # header + 2 data rows

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("CLI 'egn' with --gender female")
    def test_cli_egn_gender(self) -> None:
        output = self._run(["--seed", "42", "egn", "--gender", "female"])
        data = json.loads(output)
        egn = data["value"]
        assert int(egn[8]) % 2 == 1  # 9th digit odd = female
