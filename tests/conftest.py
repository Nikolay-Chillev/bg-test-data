"""Shared pytest fixtures for bg-test-data tests."""

from typing import Any

import pytest

from bg_test_data._random import SeededRandom
from bg_test_data.providers import BgTestData


@pytest.fixture()
def rng() -> SeededRandom:
    """Return a SeededRandom instance with a fixed seed for deterministic tests."""
    return SeededRandom(seed=42)


@pytest.fixture()
def bg() -> BgTestData:
    """Return a BgTestData facade instance with a fixed seed."""
    return BgTestData(seed=42)


@pytest.fixture()
def make_person(bg: BgTestData):
    """Factory fixture that creates persons with custom attributes."""

    def _make(**kwargs: Any) -> dict[str, Any]:
        return bg.person(**kwargs)

    return _make


@pytest.fixture()
def make_company(bg: BgTestData):
    """Factory fixture that creates companies with custom attributes."""

    def _make(**kwargs: Any) -> dict[str, Any]:
        return bg.company(**kwargs)

    return _make
