from typing import List

from mongobase.mongo_config import characters, weapons
from mongobase.schemas import Character, WeaponItem


def get_user_characters(user_id: int) -> List:
    """Get all users's characters"""
    all_characters = [
        character for character in characters.find({"owner": user_id}, {"_id": 0})
    ]
    return all_characters


def get_user_character(user_id: int, name: str) -> Character:
    """Get users's character by name"""
    character = characters.find_one({"owner": user_id, "name": name}, {"_id": 0})
    return character


def get_weapon(name: str) -> WeaponItem:
    """Get weapon by name"""
    weapon = weapons.find_one({"name": name}, {"_id": 0})
    return weapon