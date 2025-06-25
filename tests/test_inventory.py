import pytest

from src.inventory import (
    add_ingredient, list_inventory,
    remove_ingredient, update_ingredient
)

def test_remove(tmp_db):
    add_ingredient("flour", 500, "g")
    assert list_inventory() == {"flour": {"quantity": 500.0, "unit": "g"}}

    # remove it
    deleted = remove_ingredient("flour")
    assert deleted is True
    assert list_inventory() == {}

    # removing again should return False
    assert remove_ingredient("flour") is False

def test_update_quantity(tmp_db):
    add_ingredient("sugar", 100, "g")
    # bump quantity to 150
    updated = update_ingredient("sugar", qty=150)
    assert updated is True
    assert list_inventory()["sugar"]["quantity"] == 150.0
    # unit unchanged
    assert list_inventory()["sugar"]["unit"] == "g"

def test_update_unit(tmp_db):
    add_ingredient("milk", 2, "liter")
    # change only unit
    updated = update_ingredient("milk", unit="L")
    assert updated is True
    inv = list_inventory()
    assert inv["milk"] == {"quantity": 2.0, "unit": "L"}

def test_update_both(tmp_db):
    add_ingredient("eggs", 12, "count")
    updated = update_ingredient("eggs", qty=24, unit="douzaine")
    assert updated is True
    assert list_inventory()["eggs"] == {"quantity": 24.0, "unit": "douzaine"}

def test_update_missing(tmp_db):
    # nothing in DB yet
    assert update_ingredient("butter", qty=100) is False

