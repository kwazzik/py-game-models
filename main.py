import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    players = data["players"]  # Або data.get("players", data) якщо потрібно
    for nickname, player_data in players.items():
        race_data = player_data["race"]
        race_obj, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data.get("description", "")}
        )
        skills_data = race_data.get("skills", [])
        for skill in skills_data:
            Skill.objects.get_or_create(
                name=skill["name"],
                race=race_obj,
                defaults={"bonus": skill["bonus"]}
            )
        guild_data = player_data.get("guild")
        if guild_data:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")}
            )
        else:
            guild_obj = None
        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data["email"],
                "bio": player_data["bio"],
                "race": race_obj,
                "guild": guild_obj,
            }
        )


if __name__ == "__main__":
    main()
