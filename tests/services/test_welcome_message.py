from unittest.mock import MagicMock

import pytest
from discord import Guild
from omegabot.models import WelcomeMessage
from omegabot.services.welcome_message import set_welcome_message

GUILD_ID = 345
GUILD_NAME = "GUILD"
MESSAGE_STRING = "TEST_MESSAGE_STRING"


@pytest.fixture
def guild() -> Guild:
    return Guild(state=MagicMock(), data={"id": GUILD_ID, "name": GUILD_NAME})


@pytest.fixture
def database_message() -> WelcomeMessage:
    return WelcomeMessage.create(guild_id=GUILD_ID, message=MESSAGE_STRING)


def test_set_welcome_message_creates_new_welcome_message(guild: Guild):
    set_welcome_message(guild, MESSAGE_STRING)

    assert WelcomeMessage.select().count() == 1

    message: WelcomeMessage = WelcomeMessage.get(WelcomeMessage.guild_id == guild.id)
    assert message.message == MESSAGE_STRING


def test_set_welcome_message_updates_already_created_message(guild: Guild, database_message: WelcomeMessage):
    updated_message_string = MESSAGE_STRING + "_2"
    set_welcome_message(guild, updated_message_string)

    assert WelcomeMessage.select().count() == 1

    message: WelcomeMessage = WelcomeMessage.get(WelcomeMessage.guild_id == guild.id)
    assert message.message == updated_message_string
