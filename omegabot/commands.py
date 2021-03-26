import logging
from typing import List

from discord import Embed
from discord import User as DiscordUser
from discord.ext.commands import Context, has_permissions
from DiscordUtils.Pagination import CustomEmbedPaginator

from omegabot.app import bot
from omegabot.services.points import add_points
from omegabot.services.user import get_leaderboard_users, get_or_create_user

LOG = logging.getLogger(__name__)

PAGE_SIZE = 10


@bot.command()
@has_permissions(manage_guild=True)
async def give(ctx: Context, discord_user: DiscordUser, amount: int):
    LOG.info(f"Giving {amount} points to {discord_user.name}")
    command_user = get_or_create_user(ctx.author, ctx.guild)
    target_user = get_or_create_user(discord_user, ctx.guild)
    target_user = add_points(command_user, target_user, ctx.guild, amount)
    await ctx.send(f"Giving {discord_user.mention} {amount} points. They now have {target_user.points} points.")


@bot.command()
async def leaderboard(ctx: Context):
    LOG.info("Printing leaderboard")
    users = get_leaderboard_users(ctx.guild)
    paged_users = [users[i : i + PAGE_SIZE] for i in range(0, len(users), PAGE_SIZE)]
    embeds: List[Embed] = []
    for i, page in enumerate(paged_users):
        embed = Embed()
        embed.title = "Points Leaderboard"
        embed.description = "\n".join(
            [f"{i * PAGE_SIZE + j + 1}: {user.name} - {user.points}" for j, user in enumerate(page)]
        )
        embed.description += f"\n\nPage {i + 1} of {len(paged_users)}"
        embeds.append(embed)
    paginator = CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction("⏪", "back")
    paginator.add_reaction("⏩", "next")
    await paginator.run(embeds)
