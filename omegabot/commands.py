from discord import User as DiscordUser
from discord.ext.commands import Context

from omegabot.app import bot
from omegabot.services.points import add_points
from omegabot.services.user import get_or_create_user


@bot.command()
async def give(ctx: Context, discord_user: DiscordUser, amount: int):
    command_user = get_or_create_user(ctx.author)
    target_user = get_or_create_user(discord_user)
    target_user = add_points(command_user, target_user, amount)
    await ctx.send(f"Giving {discord_user.mention} {amount} points. They now have {target_user.points} points.")
