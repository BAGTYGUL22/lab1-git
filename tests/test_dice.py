import pytest
from labs.lab3.core.dice import Dice


@pytest.fixture(autouse=True)
def reset_dice():
    Dice().reseed(2026)

def test_returns_same_instance():
    first = Dice()
    second = Dice()

    assert first is second


def test_rolls_stay_within_bounds():
    low, high = 1, 6

    for _ in range(100):
        result = Dice().roll(low, high)
        assert low <= result <= high


def test_equal_bounds_return_only_value():
    value = 7
    assert Dice().roll(value, value) == value


def test_handles_certain_outcomes():
    impossible, certain = 0.0, 1.0

    for _ in range(100):
        assert Dice().chance(impossible) is False
        assert Dice().chance(certain) is True


def test_picks_only_element():
    element = object()
    assert Dice().pick([element]) is element


def test_picks_element_from_list():
    options = ["меч", "щит", "посох"]

    for _ in range(100):
        assert Dice().pick(options) in options


def test_reseed_repeats_sequence():
    seed, count = 42, 10

    Dice().reseed(seed)
    first = [Dice().roll(1, 100) for _ in range(count)]

    Dice().reseed(seed)
    repeated = [Dice().roll(1, 100) for _ in range(count)]

    assert first == repeated
