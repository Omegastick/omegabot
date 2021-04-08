from typing import List

from discord import Embed


def make_leaderboard(title: str, usernames: List[str], values: List[str], page_size: int) -> List[Embed]:
    zipped = list(zip(usernames, values))
    pages = [zipped[i : i + page_size] for i in range(0, len(zipped), page_size)]
    embeds: List[Embed] = []
    for i, page in enumerate(pages):
        embed = Embed()
        embed.title = title
        embed.description = "\n".join(
            [f"{i * page_size + j + 1}: {entry[0]} - {entry[1]}" for j, entry in enumerate(page)]
        )
        embed.description += f"\n\nPage {i + 1} of {len(pages)}"
        embeds.append(embed)
    return embeds
