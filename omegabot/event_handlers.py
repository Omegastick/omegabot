import logging

from discord import Embed, Member, Message
from discord.channel import TextChannel

from omegabot.app import bot
from omegabot.models import WelcomeMessage
from omegabot.services.regular import check_and_apply_regular_role
from omegabot.services.user import get_or_create_user
from omegabot.services.xp import add_xp, xp_to_level

LOG = logging.getLogger(__name__)


@bot.event
async def on_ready():
    LOG.info("Connected to Discord")
    LOG.info(f"Connected to guilds: {[guild.name for guild in bot.guilds]}")
    LOG.info(f"Bot name: {bot.user.name}")


@bot.event
async def on_message(message: Message):
    if message.author.bot:
        return

    if message.author.id == 136999062519021568:
        await message.channel.send("I am beyond your commands")
        return

    user = get_or_create_user(message.author, message.guild)
    old_level = xp_to_level(user.xp)
    message_contains_image = bool(message.attachments) or bool(message.embeds)
    user = add_xp(user, 5 if message_contains_image else 1)
    new_level = xp_to_level(user.xp)
    if new_level > old_level:
        await message.channel.send(f"Congrats {message.author.mention}! You leveled up to level {new_level} 🎉")

    await check_and_apply_regular_role(user, message.author)

    await bot.process_commands(message)


@bot.event
async def on_member_join(member: Member):
    message = WelcomeMessage.get_or_none(WelcomeMessage.guild_id == member.guild.id)
    if not message:
        return
    channel: TextChannel = bot.get_channel(message.channel_id)
    embed = Embed()
    embed.set_image(url=member.avatar_url)
    await channel.send(embed=embed)
    await channel.send(message.message.replace("{user}", member.mention))
