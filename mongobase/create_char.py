import json
from typing import List

from bson import json_util

from mongobase.mongo_config import characters, classes, races
from mongobase.rules import modificators, proficiency_bonuses
from mongobase.schemas import Character, SkillProficiencies, Stats
from mongobase.classes import barbarian_class, cleric_class, rogue_class
from mongobase.races import elf, human, gnome, dwarf, half_elf, half_orc, halfling, tiefling

#classes.insert_many([barbarian_class.model_dump(by_alias=True), cleric_class.model_dump(by_alias=True), rogue_class.model_dump(by_alias=True)])
#races.insert_many([elf.model_dump(by_alias=True), human.model_dump(by_alias=True), gnome.model_dump(by_alias=True), dwarf.model_dump(by_alias=True), half_elf.model_dump(by_alias=True), half_orc.model_dump(by_alias=True), halfling.model_dump(by_alias=True), tiefling.model_dump(by_alias=True)])



def get_races() -> List:
    """Get all avialable char races from database"""
    all_rases = [race for race in races.find({}, {"subraces": 0, "_id": 0 })]
    return all_rases


def get_subraces(race_name: str):
    race = races.find_one({"name": race_name}, {"subraces": 1, "_id": 0 })
    if race['subraces'] is not None:
        subraces = [subrace for subrace in race['subraces']]
    else:
        subraces = None
    return subraces


def get_classes() -> List:
    """Get all avialable char classes from database"""
    all_classes = [class_ for class_ in classes.find({}, {"name": 1, "description": 1, "_id": 0 })]
    return all_classes


def get_class_skills(class_name: str):
    character_skills = classes.find_one({"name": class_name}, {"skills": 1, "_id": 0})
    return character_skills['skills']


def create_char(char: dict):
    """Takes a dict, create Character and insert it in database"""
    character_class = classes.find_one({"name": char["character_class"]})
    character_race = races.find_one({"name": char["race"]})

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
    skills = SkillProficiencies(proficient=character_class["skills"][:2], other=[])
    hp = character_class["hit_dice"] + modificators[char["stats"]["Constitution"]]

    character = Character(
        owner=char["owner"],
        name=char["name"],
        race=char["race"],
        gender=char["gender"],
        character_class=character_class["name"],
        subclass=" ",
        level=char["level"],
        background=char["background"],
        alignment=char["alignment"],
        proficiency_bonus=proficiency_bonuses[char["level"]],
        stats=stats,
        skills=skills,
        abilities=character_class["abilities"],
        equipment=character_class["starting_equipment"],
        current_hp=hp,
        max_hp=hp,
        armor_class=10 + modificators[char["stats"]["Dexterity"]],
        initiative=modificators[char["stats"]["Dexterity"]],
        speed=character_race["speed"],
        notes=char["notes"],
    )

    characters.insert_one(character.model_dump(by_alias=True))
    print("Данные добавлены!")
