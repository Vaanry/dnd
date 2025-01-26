from typing import List
from mongo_config import characters, classes, races
from rules import modificators, proficiency_bonuses
from schemas import Character, SkillProficiencies, Stats

# from races import halfling, half_orc, half_elf, dwarf


def get_classes() -> List:
    '''Get all avialable char classes from database'''
    all_classes = [char_class["name"] for char_class in classes.find()]
    return all_classes


def get_races() -> List:
    '''Get all avialable char races from database'''
    all_rases = [race["name"] for race in races.find()]
    return all_rases


# classes.insert_many([rogue_class.model_dump(by_alias=True),
#                      cleric_class.model_dump(by_alias=True)])

# races.insert_many([halfling.model_dump(by_alias=True),
#                      half_orc.model_dump(by_alias=True),
#                      half_elf.model_dump(by_alias=True),
#                   dwarf.model_dump(by_alias=True)],
#                   )

# with open("example1.json", "r", encoding="utf-8") as file:
#     char = json.load(file)


def create_char(char: dict):
    '''Takes a dict, create Character and insert it in database'''
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
    skills = SkillProficiencies(proficient=character_class["skills"][:2],
                                other=[])
    hp = character_class["hit_dice"] + modificators[char["stats"]
                                                    ["Constitution"]]

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
