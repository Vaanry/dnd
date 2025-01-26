from typing import List, Literal, Optional

from pydantic import BaseModel


class Ability(BaseModel):
    name: str
    description: str
    level_acquired: int


class Feature(BaseModel):
    name: str
    level_acquired: int
    description: str


class Subclass(BaseModel):
    name: str
    description: str
    features: List[Feature]


# class EquipmentItem(BaseModel):
#     name: str
#     quantity: int


class CharacterClass(BaseModel):
    name: str  # Название класса, например, "Barbarian"
    description: str  # Общая информация о классе
    hit_dice: int  # Например, "d12"
    skills: List[str]  # Умения, доступные классу
    primary_stats: List[str]  # Основные характеристики, например, ["Strength"]
    saving_throws: List[str]  # Спасброски, например, ["Strength", "Constitution"]
    armor_proficiencies: List[
        str
    ]  # Например, ["Light Armor", "Medium Armor", "Shields"]
    weapon_proficiencies: List[str]  # Например, ["Simple Weapons", "Martial Weapons"]
    starting_equipment: List[str]  # Базовая экипировка
    abilities: List[Ability]  # Стартовые способности
    features: List[Feature]  # Особенности класса
    subclasses: Optional[List[Subclass]]  # Специализации (подклассы)


class Stats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class SkillProficiencies(BaseModel):
    proficient: List[str]  # Например, ["Arcana", "Nature"]
    other: List[str]  # Например, ["Perception", "Athletics"]


class Character(BaseModel):
    name: str  # Имя персонажа
    race: str  # Раса персонажа, например, "Tiefling"
    gender: Literal["Male", "Female"]  # Пол персонажа
    character_class: str  # Ссылка на модель класса
    subclass: str  # Ссылка на подкласс (если есть)
    level: int  # Уровень персонажа
    background: str  # Происхождение персонажа
    alignment: str  # Мировоззрение, например, "Chaotic Good"
    proficiency_bonus: int  # Бонус умения
    stats: Stats  # Основные характеристики
    skills: SkillProficiencies  # Умения персонажа
    abilities: List[Ability]  # Список способностей (из модели класса)
    equipment: List[str]  # Экипировка
    current_hp: int  # Текущие очки здоровья
    max_hp: int  # Максимальные очки здоровья
    armor_class: int  # Класс брони
    initiative: int  # Инициатива
    speed: int  # Скорость передвижения
    notes: Optional[str]  # Дополнительные заметки


class AbilityScoreBonus(BaseModel):
    ability: str  # Название характеристики, например, "Strength", "Dexterity"
    bonus: int  # Значение бонуса, например, 2


class RacialTrait(BaseModel):
    name: str  # Название особенности, например, "Darkvision"
    description: str  # Описание особенности


class CharacterRace(BaseModel):
    name: str  # Название расы, например, "Tiefling"
    description: str  # Общая информация о расе
    ability_score_bonuses: List[AbilityScoreBonus]  # Бонусы к характеристикам
    speed: int  # Скорость передвижения в футах
    size: str  # Размер персонажа, например, "Medium" или "Small"
    languages: List[str]  # Языки, которые знает раса
    traits: List[RacialTrait]  # Особенности расы
    subraces: Optional[
        List["CharacterRace"]
    ]  # Подрасы (например, "High Elf", "Wood Elf")
