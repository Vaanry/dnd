from typing import Dict, List

import redis

r = redis.Redis()


def set_char_init(user_id: int, char_name: str, char_race: str):
    r.hset(user_id, "char_name", char_name)
    r.hset(user_id, "char_race", char_race)


def set_char_race(user_id: int, char_race: str):
    r.hset(user_id, "char_race", char_race)


def set_char_subrace(user_id: int, char_subrace: str):
    print(char_subrace)
    if char_subrace == None:
        r.hset(user_id, "char_subrace", "None")
    else:
        r.hset(user_id, "char_subrace", char_subrace)


def set_char_class(user_id: int, char_class: str):
    r.hset(user_id, "char_class", char_class)


def set_class_skills(user_id: int, class_skills: List):
    user_skills = f"{user_id}:skills"
    for skill in class_skills:
        r.sadd(user_skills, skill)


def set_char_ctats(user_id: int, stats: Dict):
    user_stats = f"{user_id}:stats"
    for key, value in stats.items():
        r.hset(user_stats, key, value)


def get_char_info(user_id: int) -> Dict:
    user_skills = f"{user_id}:skills"
    user_stats = f"{user_id}:stats"

    char_name = r.hget(user_id, "char_name").decode("UTF-8")
    char_race = r.hget(user_id, "char_race").decode("UTF-8")
    char_subrace = r.hget(user_id, "char_subrace")
    if char_subrace.decode("UTF-8") != "None":
        char_subrace = char_subrace.decode("UTF-8")
    else:
        char_subrace = None
    char_class = r.hget(user_id, "char_class").decode("UTF-8")

    char_skills_encoded = r.smembers(user_skills)
    char_skills = [skill.decode("UTF-8") for skill in char_skills_encoded]

    char_stats_encoded = r.hgetall(user_stats)
    char_stats = {
        key.decode("UTF-8"): int(value) for key, value in char_stats_encoded.items()
    }

    char_info = {
        "char_name": char_name,
        "char_race": char_race,
        "char_subrace": char_subrace,
        "char_class": char_class,
        "char_skills": char_skills,
        "char_stats": char_stats,
    }
    print(char_info)
    return char_info
