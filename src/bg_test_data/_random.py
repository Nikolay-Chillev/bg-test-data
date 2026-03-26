"""Seeded random wrapper for reproducible test data generation."""

import random as _random_module
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class SeededRandom:
    """Thread-safe random wrapper with optional seed for reproducibility.

    Each instance maintains its own random.Random state, so multiple
    BgTestData instances with different seeds don't interfere.
    """

    def __init__(self, seed: int | None = None) -> None:
        self._seed = seed
        self._rng = _random_module.Random(seed)

    @property
    def seed(self) -> int | None:
        """Return the seed used for this instance."""
        return self._seed

    def randint(self, a: int, b: int) -> int:
        """Return random integer N such that a <= N <= b."""
        return self._rng.randint(a, b)

    def choice(self, seq: Sequence[T]) -> T:
        """Return a random element from a non-empty sequence."""
        return self._rng.choice(seq)

    def choices(self, seq: Sequence[T], k: int = 1) -> list[T]:
        """Return k random elements from a sequence with replacement."""
        return self._rng.choices(seq, k=k)

    def random(self) -> float:
        """Return a random float in [0.0, 1.0)."""
        return self._rng.random()

    def sample(self, seq: Sequence[T], k: int) -> list[T]:
        """Return k unique random elements from a sequence."""
        return self._rng.sample(list(seq), k)

    def shuffle(self, seq: list[T]) -> None:
        """Shuffle a list in place."""
        self._rng.shuffle(seq)
