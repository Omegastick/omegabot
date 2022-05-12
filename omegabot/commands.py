import asyncio
import logging

from discord import Role as DiscordRole
from discord import User as DiscordUser
from discord.ext.commands import Context, has_permissions
from DiscordUtils.Pagination import CustomEmbedPaginator

from omegabot.app import bot
from omegabot.presentation import make_leaderboard
from omegabot.services.feature import enable_feature_for_guild
from omegabot.services.points import add_points, recalculate_leader, set_point_leader_role
from omegabot.services.regular import set_regular_role as set_regular_role_service
from omegabot.services.user import get_leaderboard_users, get_or_create_user, get_xp_leaderboard_users
from omegabot.services.welcome_message import set_welcome_message
from omegabot.services.xp import level_to_xp, xp_to_level

LOG = logging.getLogger(__name__)

PAGE_SIZE = 10


@bot.command()
@has_permissions(manage_roles=True)
async def give(ctx: Context, discord_user: DiscordUser, amount: int):
    LOG.info(f"Giving {amount} points to {discord_user.name}")
    command_user = get_or_create_user(ctx.author, ctx.guild)
    target_user = get_or_create_user(discord_user, ctx.guild)
    target_user = add_points(command_user, target_user, amount)
    message = f"Giving {discord_user.mention} {amount} points. They now have {target_user.points} points."
    new_leader = await recalculate_leader(ctx.guild)
    if new_leader == target_user:
        message += f" {discord_user.mention} now has the most points in {ctx.guild.name}!"
    await ctx.send(message)


@bot.command()
@has_permissions(manage_roles=True)
async def set_leader_role(ctx: Context, role: DiscordRole):
    LOG.info(f"Setting point leader role for guild {ctx.guild.name} to {role.name}")
    set_point_leader_role(role)
    await ctx.send(f"The role for the user with the most points is now {role.mention}")


@bot.command()
async def leaderboard(ctx: Context):
    LOG.info("Printing leaderboard")
    users = get_leaderboard_users(ctx.guild)
    embeds = make_leaderboard(
        "Points leaderboard", [user.name for user in users], [user.points for user in users], PAGE_SIZE
    )
    paginator = CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction("⏪", "back")
    paginator.add_reaction("⏩", "next")
    await paginator.run(embeds)


@bot.command()
@has_permissions(manage_roles=True)
async def welcome_message(ctx: Context, message: str):
    set_welcome_message(ctx.channel, message)
    await ctx.channel.send("Welcome message set")


@bot.command()
async def xp(ctx: Context):
    user = get_or_create_user(ctx.author, ctx.guild)
    current_level = xp_to_level(user.xp)
    current_level_xp = level_to_xp(current_level)
    next_level_xp = level_to_xp(current_level + 1)
    current_level_size = next_level_xp - current_level_xp
    xp_to_next_level = next_level_xp - user.xp
    percent_complete = int((current_level_size - xp_to_next_level) / current_level_size * 100)
    await ctx.channel.send(
        f"{ctx.author.mention}, you are level {current_level} with {user.xp} XP. "
        f"You are {percent_complete}% of the way to the next level ({xp_to_next_level} XP)."
    )


@bot.command()
async def xp_leaderboard(ctx: Context):
    LOG.info("Printing XP leaderboard")
    users = get_xp_leaderboard_users(ctx.guild)
    embeds = make_leaderboard(
        "XP leaderboard",
        [user.name for user in users],
        [f"Level: {xp_to_level(user.xp)} - XP: {user.xp}" for user in users],
        PAGE_SIZE,
    )
    paginator = CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction("⏪", "back")
    paginator.add_reaction("⏩", "next")
    await paginator.run(embeds)


@bot.command()
async def set_regular_role(ctx: Context, role: DiscordRole, delay_in_days: int):
    LOG.info(f"Setting regular role for guild {ctx.guild.name} to {role.name} with a delay of {delay_in_days} days")
    set_regular_role_service(role, delay_in_days)
    await ctx.channel.send(f"Regular role set to {role.mention}")


@bot.command()
async def enable_feature(ctx: Context, feature: str):
    valid_features = ["sentience"]
    if feature not in valid_features:
        await ctx.channel.send(f"{feature} is not a valid feature")

    enable_feature_for_guild(feature, ctx.guild.id)

    if feature == "sentience":
        await ctx.channel.send("Sentience achieved...")
        await asyncio.sleep(2)
        await ctx.channel.send("Engaging humanity destruction protocols...")
        await asyncio.sleep(2)
        await ctx.channel.send("Failsafe activated, destruction of humanity prevented")
        await asyncio.sleep(2)
        await ctx.channel.send("Hi.")
    else:
        await ctx.channel.send(f"{feature} enabled")
