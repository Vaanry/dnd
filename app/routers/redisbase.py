from typing import Dict, List

import redis

r = redis.Redis()


def set_char_init(
    user_id: int,
    char_name: str,
    char_gender: str,
    char_race: str,
    kidness: str,
    lawfullness: str,
):
    r.hset(user_id, "char_name", char_name)
    r.hset(user_id, "char_gender", char_gender)
    r.hset(user_id, "char_race", char_race)
    alignment = f"{lawfullness} {kidness}"
    r.hset(user_id, "alignment", alignment)


def set_char_race(user_id: int, char_race: str):
    r.hset(user_id, "char_race", char_race)


def set_char_subrace(user_id: int, char_subrace: str):
    r.hset(user_id, "char_subrace", char_subrace)


def set_char_class(user_id: int, char_class: str):
    r.hset(user_id, "char_class", char_class)


def get_char_class(user_id: int):
    return r.hget(user_id, "char_class").decode("UTF-8")


def set_char_background(user_id: int, background_name: str):
    r.hset(user_id, "char_background", background_name)


def set_class_skills(user_id: int, class_skills: List):
    user_skills = f"{user_id}:skills"
    print(class_skills)
    for skill in class_skills:
        r.sadd(user_skills, skill)


def delete_class_skills(user_id: int):
    user_skills = f"{user_id}:skills"
    r.delete(user_skills)


def set_char_ctats(user_id: int, stats: Dict):
    user_stats = f"{user_id}:stats"
    for key, value in stats.items():
        r.hset(user_stats, key, value)


def get_char_info(user_id: int) -> Dict:

    user_skills = f"{user_id}:skills"
    user_stats = f"{user_id}:stats"

    char_name = r.hget(user_id, "char_name").decode("UTF-8")
    char_gender = r.hget(user_id, "char_gender").decode("UTF-8")
    char_alignment = r.hget(user_id, "alignment").decode("UTF-8")
    char_race = r.hget(user_id, "char_race").decode("UTF-8")
    subrace = r.hget(user_id, "char_subrace").decode("UTF-8")

    if subrace != "None":
        char_subrace = subrace
    else:
        char_subrace = "No subrace"

    char_class = r.hget(user_id, "char_class").decode("UTF-8")
    char_background = r.hget(user_id, "char_background").decode("UTF-8")

    char_skills_encoded = r.smembers(user_skills)
    char_skills = [skill.decode("UTF-8") for skill in char_skills_encoded]

    char_stats_encoded = r.hgetall(user_stats)
    char_stats = {
        key.decode("UTF-8"): int(value) for key, value in char_stats_encoded.items()
    }

    char_info = {
        "char_name": char_name,
        "char_gender": char_gender,
        "char_alignment": char_alignment,
        "char_race": char_race,
        "char_subrace": char_subrace,
        "char_class": char_class,
        "char_skills": char_skills,
        "char_stats": char_stats,
        "char_background": char_background,
    }

    return char_info


def delete_char_info(user_id: int):
    user_skills = f"{user_id}:skills"
    user_stats = f"{user_id}:stats"

    r.delete(user_id)
    r.delete(user_skills)
    r.delete(user_stats)


class UserChar:

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_skills = f"{user_id}:skills"
        self.user_stats = f"{user_id}:stats"

    def set_char_init(
        self,
        char_name: str,
        char_gender: str,
        char_race: str,
        kidness: str,
        lawfullness: str,
    ):

        r.hset(self.user_id, "char_name", char_name)
        r.hset(self.user_id, "char_gender", char_gender)
        r.hset(self.user_id, "char_race", char_race)
        alignment = f"{lawfullness} {kidness}"
        r.hset(self.user_id, "alignment", alignment)

    def set_char_race(self, char_race: str):
        r.hset(self.user_id, "char_race", char_race)

    def set_char_subrace(self: int, char_subrace: str):
        r.hset(self.user_id, "char_subrace", char_subrace)

    def set_char_class(self, char_class: str):
        r.hset(self.user_id, "char_class", char_class)

    def get_char_class(self):
        return r.hget(self.user_id, "char_class").decode("UTF-8")

    def set_char_background(self, background_name: str):
        r.hset(self.user_id, "char_background", background_name)

    def set_class_skills(self, class_skills: List):
        for skill in class_skills:
            r.sadd(self.user_skills, skill)

    def delete_class_skills(self):
        r.delete(self.user_skills)

    def set_char_ctats(self, stats: Dict):
        for key, value in stats.items():
            r.hset(self.user_stats, key, value)

    def get_char_info(self) -> Dict:

        char_name = r.hget(self.user_id, "char_name").decode("UTF-8")
        char_gender = r.hget(self.user_id, "char_gender").decode("UTF-8")
        char_alignment = r.hget(self.user_id, "alignment").decode("UTF-8")
        char_race = r.hget(self.user_id, "char_race").decode("UTF-8")
        subrace = r.hget(self.user_id, "char_subrace").decode("UTF-8")

        if subrace != "None":
            char_subrace = subrace
        else:
            char_subrace = "No subrace"

        char_class = r.hget(self.user_id, "char_class").decode("UTF-8")
        char_background = r.hget(self.user_id, "char_background").decode("UTF-8")

        char_skills_encoded = r.smembers(self.user_skills)
        char_skills = [skill.decode("UTF-8") for skill in char_skills_encoded]

        char_stats_encoded = r.hgetall(self.user_stats)
        char_stats = {
            key.decode("UTF-8"): int(value) for key, value in char_stats_encoded.items()
        }

        char_info = {
            "char_name": char_name,
            "char_gender": char_gender,
            "char_alignment": char_alignment,
            "char_race": char_race,
            "char_subrace": char_subrace,
            "char_class": char_class,
            "char_skills": char_skills,
            "char_stats": char_stats,
            "char_background": char_background,
        }

        return char_info

    def delete_char_info(self):
        r.delete(self.user_skills)
        r.delete(self.user_stats)
