from unittest.mock import MagicMock

import pytest
from discord import Guild
from discord.channel import TextChannel
from omegabot.models import WelcomeMessage
from omegabot.services.welcome_message import set_welcome_message

CHANNEL_ID = 123
CHANNEL_NAME = "TEST_CHANNEL"
GUILD_ID = 234
GUILD_NAME = "GUILD"
MESSAGE_STRING = "TEST_MESSAGE_STRING"


@pytest.fixture
def guild() -> Guild:
    return Guild(state=MagicMock(), data={"id": GUILD_ID, "name": GUILD_NAME})


@pytest.fixture
def channel(guild: Guild) -> TextChannel:
    return TextChannel(
        state=MagicMock(), guild=guild, data={"id": CHANNEL_ID, "name": CHANNEL_NAME, "type": "", "position": 0}
    )


@pytest.fixture
def database_message() -> WelcomeMessage:
    return WelcomeMessage.create(guild_id=GUILD_ID, channel_id=CHANNEL_ID, message=MESSAGE_STRING)


def test_set_welcome_message_creates_new_welcome_message(channel: TextChannel):
    set_welcome_message(channel, MESSAGE_STRING)

    assert WelcomeMessage.select().count() == 1

    message: WelcomeMessage = WelcomeMessage.get(WelcomeMessage.guild_id == channel.guild.id)
    assert message.channel_id == channel.id
    assert message.message == MESSAGE_STRING


def test_set_welcome_message_updates_already_created_message(channel: TextChannel, database_message: WelcomeMessage):
    updated_message_string = MESSAGE_STRING + "_2"
    set_welcome_message(channel, updated_message_string)

    assert WelcomeMessage.select().count() == 1

    message: WelcomeMessage = WelcomeMessage.get(WelcomeMessage.guild_id == channel.guild.id)
    assert message.channel_id == channel.id
    assert message.message == updated_message_string


def test_set_welcome_message_updates_channel_id(channel: TextChannel, database_message: WelcomeMessage):
    channel.id += 1
    set_welcome_message(channel, MESSAGE_STRING)

    message: WelcomeMessage = WelcomeMessage.get(WelcomeMessage.guild_id == channel.guild.id)
    assert message.channel_id == channel.id
