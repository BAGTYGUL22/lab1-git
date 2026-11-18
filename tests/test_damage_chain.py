
from unittest.mock import create_autospec, patch

from labs.lab3.core.dice import Dice
from labs.lab3.defense.damage import Damage
from labs.lab3.defense.damage_handler import DamageHandler
from labs.lab3.defense.evasion_handler import EvasionHandler
from labs.lab3.defense.armor_handler import ArmorHandler
from labs.lab3.defense.barrier_handler import BarrierHandler


def test_damage_passes_through_full_chain():
    # Arrange — подготовка
    dice = create_autospec(Dice, instance=True)
    dice.chance.return_value = False

    evasion = EvasionHandler(0.3)
    armor = ArmorHandler(0.25)
    barrier = BarrierHandler(10)

    final_handler = create_autospec(
        DamageHandler, instance=True
    )

    evasion.set_next(armor)
    armor.set_next(barrier)
    barrier.set_next(final_handler)

    damage = Damage(40)

    # Act — выполняем обработку
    with patch(
        "labs.lab3.defense.evasion_handler.Dice",
        return_value=dice
    ):
        evasion.handle(damage)

    # Assert — проверяем результат
    assert damage.evaded is False
    assert damage.absorbed == 10
    assert damage.amount == 20

    dice.chance.assert_called_once_with(0.3)
    final_handler.handle.assert_called_once_with(damage)
