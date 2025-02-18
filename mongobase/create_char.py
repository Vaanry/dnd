from typing import List

from mongobase.mongo_config import backgrounds, characters, classes, races
from mongobase.rules import modificators, proficiency_bonuses
from mongobase.schemas import (Character, CharacterBackground,
                               SkillProficiencies, Stats)


def get_races() -> List:
    """Get all avialable char races from database"""
    all_rases = [race for race in races.find({}, {"subraces": 0, "_id": 0})]
    return all_rases


def get_subraces(race_name: str) -> List:
    race = races.find_one({"name": race_name}, {"subraces": 1, "_id": 0})
    if race["subraces"] is not None:
        subraces = [subrace for subrace in race["subraces"]]
    else:
        subraces = None
    return subraces


def get_classes() -> List:
    """Get all avialable char classes from database"""
    all_classes = [
        class_ for class_ in classes.find({}, {"name": 1, "description": 1, "_id": 0})
    ]
    return all_classes


def get_class_skills(class_name: str) -> List:
    character_skills = classes.find_one({"name": class_name}, {"skills": 1, "_id": 0})
    return character_skills["skills"]


def get_class_equipment(class_name: str) -> List:
    class_ = classes.find_one({"name": class_name}, {"starting_equipment": 1, "_id": 0})
    return class_["starting_equipment"]


def get_backgrounds() -> List:
    """Get all avialable backgrounds from database"""
    all_backgrounds = [background for background in backgrounds.find({}, {"_id": 0})]
    return all_backgrounds


def get_background_skills(background_name: str) -> List:
    character_skills = backgrounds.find_one(
        {"name": background_name}, {"skill_proficiencies": 1, "_id": 0}
    )
    return character_skills["skill_proficiencies"]


def create_char(char: dict):
    """Takes a dict, create Character and insert it in database"""
    character_class = classes.find_one({"name": char["character_class"]})
    character_race = races.find_one({"name": char["race"]})

    character_background = backgrounds.find_one({"name": char["background"]})
    background_equipment = [item["name"] for item in character_background["equipment"]]
    char_languages = set()

    if char["subrace"] != "No subrace":  # char["subrace"]
        result = races.find_one(
            {"subraces": {"$elemMatch": {"name": char["subrace"]}}},
            {"languages": 1, "_id": 0},
        )
        subrace_lang = result["languages"]
        char_languages.update(subrace_lang)
    else:
        char_languages.update(character_race["languages"])

    if character_background["languages"] is not None:
        char_languages.update(character_background["languages"])

    for ability in character_race["ability_score_bonuses"]:
        name = ability["ability"]
        bonus = ability["bonus"]
        char["stats"][name] += bonus

    stats = Stats(
        strength=char["stats"]["Strength"],
        dexterity=char["stats"]["Dexterity"],
        constitution=char["stats"]["Constitution"],
        intelligence=char["stats"]["Intelligence"],
        wisdom=char["stats"]["Wisdom"],
        charisma=char["stats"]["Charisma"],
    )
    skills = SkillProficiencies(proficient=char["skills"], other=[])
    hp = character_class["hit_dice"] + modificators[char["stats"]["Constitution"]]

    character = Character(
        owner=char["owner"],
        name=char["name"],
        race=char["race"],
        subrace=char["subrace"],
        gender=char["gender"],
        character_class=character_class["name"],
        subclass=" ",
        level=char["level"],
        experience=0,
        background=character_background["name"],
        alignment=char["alignment"],
        proficiency_bonus=proficiency_bonuses[char["level"]],
        stats=stats,
        skills=skills,
        abilities=character_class["abilities"],
        armor=char["armor"],
        weapon=char["weapon"],
        equipment=char["equipment"] + background_equipment,
        current_hp=hp,
        max_hp=hp,
        armor_class=10 + modificators[char["stats"]["Dexterity"]],
        initiative=modificators[char["stats"]["Dexterity"]],
        speed=character_race["speed"],
        languages=list(char_languages),
        notes=char["notes"],
    )

    characters.insert_one(character.model_dump(by_alias=True))
    print("Данные добавлены!")
