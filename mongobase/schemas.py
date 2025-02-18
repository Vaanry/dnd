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


class EquipmentItem(BaseModel):
    name: str
    quantity: int
    cost: int  # Стоимость(в золотых монетах)


class MoneyItem(BaseModel):
    name: str  # Тип монет (золотые, серебряные, медные и тд)
    quantity: int


class ArmorItem(BaseModel):
    name: str  # Название доспеха
    armor_type: Literal[
        "light", "medium", "heavy", "shield"
    ]  # Тип доспеха (легкий, средний, тяжелый)
    cost: int  # Стоимость доспеха (в золотых монетах)
    armor_class: int  # Класс брони
    strength_required: Optional[int] = None  # Требуется сила (если есть)
    disadvantage: Optional[bool] = None  # Помеха (если есть)


class Damage(BaseModel):
    amount: str  # Например, "1d6", "1d10"
    damage_type: str  # Например, "bludgeoning", "fire", "piercing", etc.


class WeaponItem(BaseModel):
    name: str  # Название оружия, например, "Longsword", "Bow"
    attack_type: Literal[
        "melee", "ranged"
    ]  # Тип атаки: "melee" (рукопашное) или "ranged" (дальнобойное)
    weapon_category: Literal[
        "martial", "simple"
    ]  # Тип оружия: "martial" (воинское) или "simple" (простое)
    damage: List[Damage]  # Список возможных типов урона для оружия
    properties: List[str]  # Список свойств оружия: например, "thrown", "light", etc.
    range: Optional[int] = (
        None  # Дистанция для дальнобойного оружия (опционально, только для ranged)
    )
    cost: int  # Стоимость


class EquipmentSet(BaseModel):
    armor: Optional[List[ArmorItem]]
    weapon: Optional[List[WeaponItem]]
    other: Optional[List[EquipmentItem]]


class CharacterClass(BaseModel):
    # owner: int  # ID владельца персонажа
    name: str  # Название класса, например, "Barbarian"
    description: str  # Общая информация о классе
    hit_dice: int  # Например, "d12"
    skills: List[str]  # Умения, доступные классу
    primary_stats: List[str]  # Основные характеристики, например, ["Strength"]
    saving_throws: List[str]  # Спасброски, напр., ["Strength", "Constitution"]
    armor_proficiencies: List[
        str
    ]  # Например, ["Light Armor", "Medium Armor", "Shields"]
    weapon_proficiencies: List[str]  # Например, ["Simple Weapons"]
    starting_equipment: List[EquipmentSet]  # Базовая экипировка
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


class CharacterBackground(BaseModel):
    name: str  # Название происхождения, например, "Acolyte" (Послушник)
    description: str  # Общая информация
    skill_proficiencies: List[str]  # Владение навыками
    tool_proficiencies: Optional[List[str]] = (
        None  # Владение инструментами (опционально)
    )
    languages: Optional[List[str]] = None  # Языки (опционально, от 0 до 3)
    equipment: List[EquipmentItem]  # Стартовое снаряжение
    money: List[MoneyItem]


class Character(BaseModel):
    owner: int  # Владелец персонажа
    name: str  # Имя персонажа
    race: str  # Раса персонажа, например, "Tiefling"
    subrace: str  # Подраса персонажа
    gender: Literal["Male", "Female"]  # Пол персонажа
    character_class: str  # Ссылка на модель класса
    subclass: str  # Ссылка на подкласс (если есть)
    level: int  # Уровень персонажа
    experience: int
    background: str  # Происхождение персонажа
    alignment: str  # Мировоззрение, например, "Chaotic Good"
    proficiency_bonus: int  # Бонус умения
    stats: Stats  # Основные характеристики
    skills: SkillProficiencies  # Умения персонажа
    abilities: List[Ability]  # Список способностей (из модели класса)
    armor: Optional[List[str]]
    weapon: Optional[List[str]]
    equipment: Optional[List[str]]  # Экипировка
    current_hp: int  # Текущие очки здоровья
    max_hp: int  # Максимальные очки здоровья
    armor_class: int  # Класс брони
    initiative: int  # Инициатива
    speed: int  # Скорость передвижения
    languages: List[str]
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
