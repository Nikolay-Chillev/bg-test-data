"""Tests for export utilities (JSON, CSV, dict)."""

import csv
import json
from pathlib import Path

import allure

from bg_test_data.export import to_csv, to_csv_file, to_dict, to_json
from bg_test_data.providers import BgTestData


@allure.epic("bg-test-data")
@allure.feature("Export Utilities")
class TestExport:
    """Tests for data serialization functions."""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("to_json produces valid JSON")
    def test_to_json_valid_json(self, bg: BgTestData) -> None:
        person = bg.person()
        json_str = to_json(person)
        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)
        assert parsed["egn"] == person["egn"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("to_json preserves Cyrillic characters by default")
    def test_to_json_cyrillic(self, bg: BgTestData) -> None:
        person = bg.person()
        json_str = to_json(person)
        first_name = str(person["first_name"])
        assert first_name in json_str, "Cyrillic name should appear as-is in JSON output"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("to_json serializes list of dicts")
    def test_to_json_list(self, bg: BgTestData) -> None:
        persons = bg.persons(count=3)
        json_str = to_json(persons)
        parsed = json.loads(json_str)
        assert isinstance(parsed, list)
        assert len(parsed) == 3

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("to_csv includes header row with field names")
    def test_to_csv_headers(self, bg: BgTestData) -> None:
        person = bg.person()
        csv_str = to_csv(person)
        lines = csv_str.strip().split("\n")
        assert len(lines) >= 2, "CSV should have at least a header and one data row"
        header = lines[0]
        assert "egn" in header
        assert "gender" in header

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("to_csv with multiple records has correct row count")
    def test_to_csv_multiple_records(self, bg: BgTestData) -> None:
        persons = bg.persons(count=5)
        csv_str = to_csv(persons)
        lines = csv_str.strip().split("\n")
        assert len(lines) == 6  # 1 header + 5 data rows

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("to_csv_file writes valid CSV to disk")
    def test_to_csv_file_writes_to_disk(self, bg: BgTestData, tmp_path: Path) -> None:
        persons = bg.persons(count=3)
        filepath = str(tmp_path / "test_output.csv")
        to_csv_file(persons, filepath)

        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 4  # 1 header + 3 data rows
        assert "egn" in rows[0]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("to_dict returns the same data unchanged")
    def test_to_dict_passthrough(self, bg: BgTestData) -> None:
        person = bg.person()
        result = to_dict(person)
        assert result is person

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("to_dict passes through list unchanged")
    def test_to_dict_list_passthrough(self, bg: BgTestData) -> None:
        persons = bg.persons(count=2)
        result = to_dict(persons)
        assert result is persons
