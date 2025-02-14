from typing import List

from mongobase.mongo_config import characters
from mongobase.schemas import Character


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
