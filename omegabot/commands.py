from discord import User as DiscordUser
from discord.ext.commands import Context

from omegabot.app import bot
from omegabot.models.user import User


@bot.command()
async def test(ctx: Context, *args):
    await ctx.send(args)


@bot.command()
async def give(ctx: Context, discord_user: DiscordUser, amount: int):
    user, _ = User.get_or_create(id=discord_user.id)
    user.points += amount
    user.save()
    await ctx.send(f"Giving {discord_user.mention} {amount} points. They now have {user.points}.")
