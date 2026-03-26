"""Tests for the SeededRandom wrapper."""

import allure
import pytest

from bg_test_data._random import SeededRandom


@allure.epic("bg-test-data")
@allure.feature("SeededRandom")
class TestSeededRandom:
    """Tests for SeededRandom deterministic behavior and core methods."""

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Same seed produces identical output sequence")
    def test_seed_determinism(self) -> None:
        rng1 = SeededRandom(seed=42)
        rng2 = SeededRandom(seed=42)

        values1 = [rng1.randint(0, 1000) for _ in range(50)]
        values2 = [rng2.randint(0, 1000) for _ in range(50)]

        assert values1 == values2

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("No seed produces varying output across instances")
    def test_no_seed_varies(self) -> None:
        rng1 = SeededRandom(seed=None)
        rng2 = SeededRandom(seed=None)

        # Generate enough values that collisions are astronomically unlikely
        values1 = [rng1.randint(0, 10**9) for _ in range(20)]
        values2 = [rng2.randint(0, 10**9) for _ in range(20)]

        assert values1 != values2

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("randint returns values within the specified range")
    @pytest.mark.parametrize("low,high", [(0, 10), (1, 1), (-100, 100), (0, 0)])
    def test_randint_range(self, low: int, high: int) -> None:
        rng = SeededRandom(seed=7)
        for _ in range(100):
            value = rng.randint(low, high)
            assert low <= value <= high

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("choice returns an element from the provided list")
    def test_choice_from_list(self) -> None:
        rng = SeededRandom(seed=7)
        items = ["a", "b", "c", "d"]
        for _ in range(100):
            assert rng.choice(items) in items

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("seed property returns the seed used at construction")
    def test_seed_property(self) -> None:
        rng = SeededRandom(seed=99)
        assert rng.seed == 99

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("seed property is None when no seed provided")
    def test_seed_property_none(self) -> None:
        rng = SeededRandom()
        assert rng.seed is None
