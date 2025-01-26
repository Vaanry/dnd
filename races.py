from schemas import AbilityScoreBonus, CharacterRace, RacialTrait

# Бонусы характеристик

gnome_bonus = AbilityScoreBonus(ability="Intelligence", bonus=2)
elf_bonus = AbilityScoreBonus(ability="Dexterity", bonus=2)
human_bonus = [
    AbilityScoreBonus(ability="Strength", bonus=1),
    AbilityScoreBonus(ability="Dexterity", bonus=1),
    AbilityScoreBonus(ability="Constitution", bonus=1),
    AbilityScoreBonus(ability="Intelligence", bonus=1),
    AbilityScoreBonus(ability="Wisdom", bonus=1),
    AbilityScoreBonus(ability="Charisma", bonus=1),
]
tiefling_bonus = [
    AbilityScoreBonus(ability="Charisma", bonus=2),
    AbilityScoreBonus(ability="Intelligence", bonus=1),
]
dwarf_bonus = AbilityScoreBonus(ability="Constitution", bonus=2)
half_elf_bonus = AbilityScoreBonus(ability="Charisma", bonus=2)
half_orc_bonus = AbilityScoreBonus(ability="Strength", bonus=2)
halfling_bonus = AbilityScoreBonus(ability="Dexterity", bonus=2)


# Черты
gnome_traits = [
    RacialTrait(name="Darkvision", description="Can see in the dark up to 60 feet."),
    RacialTrait(
        name="Gnome Cunning",
        description="Advantage on Intelligence, Wisdom, and Charisma saving throws against magic.",
    ),
]
elf_traits = [
    RacialTrait(name="Darkvision", description="Can see in the dark up to 60 feet."),
    RacialTrait(
        name="Fey Ancestry",
        description="Advantage on saving throws against being charmed, and magic can’t put you to sleep.",
    ),
    RacialTrait(
        name="Trance",
        description="Elves don’t need to sleep. They meditate deeply for 4 hours a day.",
    ),
]
human_traits = [
    RacialTrait(
        name="Human Versatility",
        description="Humans gain proficiency in one skill of their choice.",
    )
]
dwarf_traits = [
    RacialTrait(name="Darkvision", description="Can see in the dark up to 60 feet."),
    RacialTrait(
        name="Dwarven Resilience",
        description="Advantage on saving throws against poison and resistance to poison damage.",
    ),
    RacialTrait(
        name="Stonecunning",
        description="Proficiency in History checks related to the origin of stonework.",
    ),
]
half_elf_traits = [
    RacialTrait(name="Darkvision", description="Can see in the dark up to 60 feet."),
    RacialTrait(
        name="Fey Ancestry",
        description="Advantage on saving throws against being charmed, and magic can’t put you to sleep.",
    ),
    RacialTrait(
        name="Skill Versatility",
        description="Proficiency in two skills of your choice.",
    ),
]
half_orc_traits = [
    RacialTrait(name="Darkvision", description="Can see in the dark up to 60 feet."),
    RacialTrait(
        name="Relentless Endurance",
        description="When reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead once per long rest.",
    ),
    RacialTrait(
        name="Savage Attacks",
        description="When you score a critical hit with a melee weapon attack, you can roll one additional damage die.",
    ),
]
halfling_traits = [
    RacialTrait(
        name="Lucky",
        description="When you roll a 1 on an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.",
    ),
    RacialTrait(
        name="Brave",
        description="You have advantage on saving throws against being frightened.",
    ),
    RacialTrait(
        name="Halfling Nimbleness",
        description="You can move through the space of any creature that is of a size larger than yours.",
    ),
]
# Экземпляры рас
gnome = CharacterRace(
    name="Gnome",
    description="Gnomes are small, intelligent creatures known for their curiosity and inventiveness.",
    ability_score_bonuses=[gnome_bonus],
    speed=25,
    size="Small",
    languages=["Common", "Gnome"],
    traits=gnome_traits,
    subraces=None,
)

elf = CharacterRace(
    name="Elf",
    description="Elves are graceful, long-lived creatures with keen senses and an affinity for magic.",
    ability_score_bonuses=[elf_bonus],
    speed=30,
    size="Medium",
    languages=["Common", "Elvish"],
    traits=elf_traits,
    subraces=[
        CharacterRace(
            name="High Elf",
            description="High Elves are more magically inclined, and have a natural affinity for arcane magic.",
            ability_score_bonuses=[AbilityScoreBonus(ability="Intelligence", bonus=1)],
            speed=30,
            size="Medium",
            languages=["Common", "Elvish", "One additional language of choice"],
            traits=[
                RacialTrait(
                    name="Cantrip",
                    description="Know one cantrip of your choice from the Wizard spell list.",
                )
            ],
            subraces=None,
        ),
        CharacterRace(
            name="Wood Elf",
            description="Wood Elves are in tune with nature, known for their speed and stealth in natural environments.",
            ability_score_bonuses=[AbilityScoreBonus(ability="Wisdom", bonus=1)],
            speed=35,
            size="Medium",
            languages=["Common", "Elvish"],
            traits=[
                RacialTrait(
                    name="Mask of the Wild",
                    description="Can hide when lightly obscured by natural phenomena.",
                )
            ],
            subraces=None,
        ),
    ],
)

human = CharacterRace(
    name="Human",
    description="Humans are versatile and adaptive, capable of thriving in any environment.",
    ability_score_bonuses=human_bonus,
    speed=30,
    size="Medium",
    languages=["Common"],
    traits=human_traits,
    subraces=None,
)


tiefling = CharacterRace(
    name="Tiefling",
    description="Descendants of infernal beings, Tieflings are known for their fiendish heritage.",
    ability_score_bonuses=tiefling_bonus,
    speed=30,
    size="Medium",
    languages=["Common", "Infernal"],
    traits=[
        RacialTrait(
            name="Darkvision", description="You can see in darkness up to 60 feet."
        ),
        RacialTrait(
            name="Hellish Resistance", description="You have resistance to fire damage."
        ),
        RacialTrait(
            name="Infernal Legacy", description="You know the *Thaumaturgy* cantrip."
        ),
    ],
    subraces=None,
)
dwarf = CharacterRace(
    name="Dwarf",
    description="Dwarves are sturdy and resilient, known for their skill in crafting and their strong connection to stone.",
    ability_score_bonuses=[dwarf_bonus],
    speed=25,
    size="Medium",
    languages=["Common", "Dwarvish"],
    traits=dwarf_traits,
    subraces=[
        CharacterRace(
            name="Hill Dwarf",
            description="Hill Dwarves are known for their endurance and resilience, gaining additional wisdom.",
            ability_score_bonuses=[AbilityScoreBonus(ability="Wisdom", bonus=1)],
            speed=25,
            size="Medium",
            languages=["Common", "Dwarvish"],
            traits=[
                RacialTrait(
                    name="Dwarven Toughness",
                    description="Hit point maximum increases by 1, and it increases by 1 every time you gain a level.",
                )
            ],
            subraces=None,
        ),
        CharacterRace(
            name="Mountain Dwarf",
            description="Mountain Dwarves are known for their physical strength and skill in combat, especially with heavy armor.",
            ability_score_bonuses=[AbilityScoreBonus(ability="Strength", bonus=2)],
            speed=25,
            size="Medium",
            languages=["Common", "Dwarvish"],
            traits=[
                RacialTrait(
                    name="Dwarven Armor Training",
                    description="Proficiency with light and medium armor.",
                )
            ],
            subraces=None,
        ),
    ],
)

half_elf = CharacterRace(
    name="Half-Elf",
    description="Half-Elves are a mix of human and elven heritage, and they combine the best traits of both races.",
    ability_score_bonuses=[half_elf_bonus],
    speed=30,
    size="Medium",
    languages=["Common", "Elvish"],
    traits=half_elf_traits,
    subraces=None,
)

half_orc = CharacterRace(
    name="Half-Orc",
    description="Half-Orcs are strong and fierce warriors, born from the union of humans and orcs.",
    ability_score_bonuses=[half_orc_bonus],
    speed=30,
    size="Medium",
    languages=["Common", "Orc"],
    traits=half_orc_traits,
    subraces=None,
)

halfling = CharacterRace(
    name="Halfling",
    description="Halflings are small and quick, known for their good luck and nimbleness.",
    ability_score_bonuses=[halfling_bonus],
    speed=25,
    size="Small",
    languages=["Common", "Halfling"],
    traits=halfling_traits,
    subraces=[
        CharacterRace(
            name="Lightfoot Halfling",
            description="Lightfoot Halflings are known for their ability to hide and move unnoticed.",
            ability_score_bonuses=[AbilityScoreBonus(ability="Charisma", bonus=1)],
            speed=25,
            size="Small",
            languages=["Common", "Halfling"],
            traits=[
                RacialTrait(
                    name="Naturally Stealthy",
                    description="You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.",
                )
            ],
            subraces=None,
        ),
        CharacterRace(
            name="Stout Halfling",
            description="Stout Halflings are tough and resilient, with a natural resistance to poison.",
            ability_score_bonuses=[AbilityScoreBonus(ability="Constitution", bonus=1)],
            speed=25,
            size="Small",
            languages=["Common", "Halfling"],
            traits=[
                RacialTrait(
                    name="Stout Resilience",
                    description="You have advantage on saving throws against poison, and you have resistance to poison damage.",
                )
            ],
            subraces=None,
        ),
    ],
)
