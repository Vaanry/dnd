from mongobase.items import (barbarian_set_1, barbarian_set_2, cleric_1,
                             cleric_2, rogue_1, rogue_2)
from mongobase.schemas import Ability, CharacterClass, Feature, Subclass

cleric_class = CharacterClass(
    name="Cleric",
    description="A priestly champion who wields divine magic in service of a higher power.",
    hit_dice=8,  # d8
    skills=["Religion", "Medicine", "History", "Insight"],
    primary_stats=["Wisdom"],
    saving_throws=["Wisdom", "Charisma"],
    armor_proficiencies=["Light Armor", "Medium Armor", "Shields"],
    weapon_proficiencies=["Simple Weapons"],
    starting_equipment=[cleric_1, cleric_2],
    abilities=[
            {"name": "Divine Domain",
            "description": "Choose a domain related to your deity, granting unique abilities.",
            "level_acquired": 1,}
        ,
            {"name": "Channel Divinity",
            "description": "Invoke divine energy to perform powerful effects.",
            "level_acquired": 2,}
        ,
    ],
    features=[
            {"name": "Spellcasting",
            "level_acquired": 1,
            "description": "Allows the casting of divine spells."},
        
            {"name": "Divine Intervention",
            "level_acquired": 10,
            "description": "Request your deity's aid in critical moments."},
        
    ],
    subclasses=[
        {
            "name": "Life Domain",
            "description": "Focused on healing and sustaining life.",
            "features": [

                    {"name": "Disciple of Life",
                    "level_acquired": 1,
                    "description": "Boosts healing spells' effectiveness."}
                ,

                    {"name": "Preserve Life",
                    "level_acquired": 2,
                    "description": "Restore hit points to creatures within range."}
                ,
            ],
        }
    ]
)

rogue_class = CharacterClass(
    name="Rogue",
    description="A scoundrel who uses stealth and trickery to overcome obstacles and enemies.",
    hit_dice=8,  # d8
    skills=["Stealth", "Acrobatics", "Deception", "Sleight of Hand"],
    primary_stats=["Dexterity"],
    saving_throws=["Dexterity", "Intelligence"],
    armor_proficiencies=["Light Armor"],
    weapon_proficiencies=[
        "Simple Weapons",
        "Hand Crossbows",
        "Longswords",
        "Rapiers",
        "Shortswords",
    ],
    starting_equipment=[rogue_1, rogue_2],
    abilities=[
        {
            "name": "Expertise",
            "description": "Double your proficiency bonus for chosen skills.",
            "level_acquired": 1,
        },
        {
            "name": "Sneak Attack",
            "description": "Deal extra damage to a creature you hit with an attack when certain conditions are met.",
            "level_acquired": 1,
        },
    ],
    features=[
        {
            "name": "Cunning Action",
            "level_acquired": 2,
            "description": "Take a bonus action to Dash, Disengage, or Hide.",
        },
        {
            "name": "Uncanny Dodge",
            "level_acquired": 5,
            "description": "Reduce damage from attacks you can see.",
        },
    ],
    subclasses=[
        {
            "name": "Thief",
            "description": "Specialized in nimbleness and acquiring objects.",
            "features": [
                {
                    "name": "Fast Hands",
                    "level_acquired": 3,
                    "description": "Use the Use an Object action as a bonus action.",
                },
                {
                    "name": "Second-Story Work",
                    "level_acquired": 3,
                    "description": "Climb faster and jump farther.",
                },
            ],
        }
    ],
)


barbarian_class = CharacterClass(
    name="Barbarian",
    description="A fierce warrior of primitive background who can enter a battle rage.",
    hit_dice=12,
    skills=["Athletics", "Intimidation"],
    primary_stats=["Strength"],
    saving_throws=["Strength", "Constitution"],
    armor_proficiencies=["Light Armor", "Medium Armor", "Shields"],
    weapon_proficiencies=["Simple Weapons", "Martial Weapons"],
    starting_equipment=[barbarian_set_1, barbarian_set_2],
    abilities=[
        Ability(
            name="Rage",
            description="Increases damage dealt and provides resistance to damage.",
            level_acquired=1,
        ),
        Ability(
            name="Unarmored Defense",
            description="Allows higher AC when not wearing armor.",
            level_acquired=1,
        ),
    ],
    features=[
        Feature(
            name="Extra Attack",
            level_acquired=5,
            description="Allows one additional attack on your turn.",
        ),
        Feature(
            name="Fast Movement",
            level_acquired=5,
            description="Increases walking speed by 10 feet.",
        ),
    ],
    subclasses=[
        Subclass(
            name="Path of the Berserker",
            description="A path of unrelenting fury.",
            features=[
                Feature(
                    name="Frenzy",
                    level_acquired=3,
                    description="Allows a bonus attack while raging.",
                ),
                Feature(
                    name="Mindless Rage",
                    level_acquired=6,
                    description="Cannot be charmed or frightened while raging.",
                ),
            ],
        )
    ],
)