from unittest.mock import create_autospec

from labs.lab3.storage.hero_repository import HeroRepository
from labs.lab3.storage.caching_hero_repository import CachingHeroRepository
from labs.lab3.hero.hero import Hero
from labs.lab3.hero.hero_class import HeroClass
from labs.lab3.item.default_catalog import create_default_catalog


def warrior(name):
    return (
        Hero.Builder()
        .set_name(name)
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(
            HeroClass.WARRIOR.starter_kit(create_default_catalog())
        )
        .build()
    )



def test_loads_lazily():
    storage = create_autospec(HeroRepository, instance=True)

    CachingHeroRepository(storage)

    assert storage.mock_calls == []


def test_reads_storage_only_once():
    storage = create_autospec(HeroRepository, instance=True)
    hero = warrior("Артур")
    storage.find_all.return_value = [hero]

    cache = CachingHeroRepository(storage)

    first = cache.find_by_name("Артур")
    second = cache.find_by_name("Артур")
    assert first is hero
    assert second is first
    storage.find_all.assert_called_once_with()


def test_caches_empty_storage():
    storage = create_autospec(HeroRepository, instance=True)
    storage.find_all.return_value = []

    cache = CachingHeroRepository(storage)

    assert cache.find_by_name("Никто") is None
    assert cache.find_by_name("Никто") is None
    storage.find_all.assert_called_once_with()


def test_saves_to_storage_and_updates_cache():
    storage = create_autospec(HeroRepository, instance=True)

    old_hero = warrior("Артур")
    storage.find_all.return_value = [old_hero]

    cache = CachingHeroRepository(storage)
    assert cache.find_by_name("Артур") is old_hero

    updated = warrior("Артур")
    updated.add_gold(100)

    cache.save(updated)

    storage.save.assert_called_once_with(updated)
    assert cache.find_by_name("Артур") is updated
    storage.find_all.assert_called_once_with()
