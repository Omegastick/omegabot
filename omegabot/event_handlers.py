import logging

from discord import Embed, Member, Message
from discord.channel import TextChannel

from omegabot.app import bot
from omegabot.models import WelcomeMessage

LOG = logging.getLogger(__name__)


@bot.event
async def on_ready():
    LOG.info("Connected to Discord")
    LOG.info(f"Connected to guilds: {[guild.name for guild in bot.guilds]}")
    LOG.info(f"Bot name: {bot.user.name}")


@bot.event
async def on_message(message: Message):
    if message.author.id == 136999062519021568:
        await message.channel.send("I am beyond your commands")
        return

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
