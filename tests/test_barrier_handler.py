import pytest

from labs.lab3.defense.barrier_handler import BarrierHandler
from labs.lab3.defense.damage import Damage


def damage_cases():
    return [
        (0, 0, 0),
        (10, 10, 0),
        (30, 30, 0),
        (40, 30, 10)
    ]


@pytest.mark.parametrize(
    "incoming, absorbed, remaining",
    damage_cases()
)
def test_handles_damage_boundaries(incoming, absorbed, remaining):
    # Arrange — подготовка
    barrier = BarrierHandler(30)
    damage = Damage(incoming)

    # Act — действие
    barrier.handle(damage)

    # Assert — проверка
    assert damage.absorbed == absorbed
    assert damage.amount == remaining


def test_spends_capacity_across_hits():
    barrier = BarrierHandler(30)

    first = Damage(20)
    second = Damage(20)
    third = Damage(20)

    barrier.handle(first)
    barrier.handle(second)
    barrier.handle(third)

    assert (first.absorbed, first.amount) == (20, 0)
    assert (second.absorbed, second.amount) == (10, 10)
    assert (third.absorbed, third.amount) == (0, 20)
