from unittest.mock import Mock

import pytest
from omegabot.services.openai import (
    NameMentionMapping,
    convert_mentions_to_names,
    convert_names_to_mentions,
    create_name_mention_mapping_from_history,
)

MENTIONS_CHATLOG = """<@!352441938898583555>: <@823594448499638302> <a:dance:864508555008147477>
<@!151628695650435072>: HAHAHAHA
<@823594448499638302>: <@!352441938898583555> do you dance?
<@!151628695650435072>: <@!352441938898583555> do you dance?
<@!352441938898583555>: https://tenor.com/view/skeleton-meme-ryder-dance-gif-21810902
<@!352441938898583555>: <@823594448499638302> do you dance???
<@823594448499638302>: <@!352441938898583555> do you dance?
<@!352441938898583555>: <@823594448499638302> lil boogie
<@823594448499638302>: <@!352441938898583555> do you dance?
<@155833230098956289>: <@823594448499638302> Who's hotter, deez nuts or the sun?
<@823594448499638302>:"""

NAMES_CHATLOG = """@e-girl#2: @Omegabot <a:dance:864508555008147477>
@e-girl#1: HAHAHAHA
@Omegabot: @e-girl#2 do you dance?
@e-girl#1: @e-girl#2 do you dance?
@e-girl#2: https://tenor.com/view/skeleton-meme-ryder-dance-gif-21810902
@e-girl#2: @Omegabot do you dance???
@Omegabot: @e-girl#2 do you dance?
@e-girl#2: @Omegabot lil boogie
@Omegabot: @e-girl#2 do you dance?
@Jr: @Omegabot Who's hotter, deez nuts or the sun?
@Omegabot:"""


@pytest.fixture
def name_mention_mapping() -> NameMentionMapping:
    return NameMentionMapping(
        names=["@e-girl#1", "@e-girl#2", "@e-girl#2", "@Jr", "@Omegabot"],
        mentions=[
            "<@!151628695650435072>",
            "<@!352441938898583555>",
            "<@352441938898583555>",
            "<@155833230098956289>",
            "<@823594448499638302>",
        ],
    )


def test_convert_mentions_to_names(name_mention_mapping: NameMentionMapping):
    assert convert_mentions_to_names(MENTIONS_CHATLOG, name_mention_mapping) == NAMES_CHATLOG


def test_convert_names_to_mentions(name_mention_mapping: NameMentionMapping):
    assert convert_names_to_mentions(NAMES_CHATLOG, name_mention_mapping) == MENTIONS_CHATLOG


def test_create_name_mention_mapping_from_history():
    authors = [
        Mock(display_name="e-girl#1", mention="<@!151628695650435072>"),
        Mock(display_name="e-girl#2", mention="<@!352441938898583555>"),
        Mock(display_name="Jr", mention="<@155833230098956289>"),
    ]
    history = [
        Mock(author=authors[0], mentions=[authors[1], authors[0]]),
        Mock(author=authors[2], mentions=[authors[0]]),
    ]
    mapping = create_name_mention_mapping_from_history(history)
    assert set(mapping.list_names()) == {"@e-girl#1", "@e-girl#2", "@Jr"}
    assert mapping.get_name("<@!151628695650435072>") == "@e-girl#1"
    assert mapping.get_mention("@Jr") in ["<@155833230098956289>", "<@!155833230098956289>"]
