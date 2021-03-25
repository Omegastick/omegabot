import logging
from typing import List

from discord import Embed
from discord import User as DiscordUser
from discord.ext.commands import Context, has_permissions

from omegabot.app import bot
from omegabot.models import User
from omegabot.services.points import add_points
from omegabot.services.user import get_or_create_user

LOG = logging.getLogger(__name__)


@bot.command()
@has_permissions(manage_guild=True)
async def give(ctx: Context, discord_user: DiscordUser, amount: int):
    LOG.info(f"Giving {amount} points to {discord_user.name}")
    command_user = get_or_create_user(ctx.author)
    target_user = get_or_create_user(discord_user)
    target_user = add_points(command_user, target_user, amount)
    await ctx.send(f"Giving {discord_user.mention} {amount} points. They now have {target_user.points} points.")


@bot.command()
async def leaderboard(ctx: Context):
    LOG.info("Printing leaderboard")
    users: List[User] = User.select().order_by(User.points.desc())
    embed = Embed()
    embed.title = "Points Leaderboard"
    embed.description = "\n".join([f"{user.name} - {user.points}" for user in users])
    await ctx.send(embed=embed)
