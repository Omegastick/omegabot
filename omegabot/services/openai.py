import logging
import os
import re
from collections import defaultdict
from typing import List, cast

from discord import Member, Message

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

LOG = logging.getLogger(__name__)


class NameMentionMapping:
    def __init__(self, names: List[str], mentions: List[str]):
        zipped = list(zip(mentions, names))
        self.mention_to_name = {mention: name for mention, name in zipped}
        self.name_to_mention = defaultdict(list)
        for mention, name in zipped:
            self.name_to_mention[name].append(mention)

    def get_name(self, mention: str) -> str:
        return self.mention_to_name[mention]

    def get_mention(self, name: str) -> str:
        return self.name_to_mention[name][0]

    def list_names(self) -> List[str]:
        return list(self.name_to_mention.keys())


def get_prediction(prompt: str, **args) -> str:
    LOG.info(f"Getting prediction for prompt: {prompt}")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        **args,
    )
    return response["choices"][0]["text"]


def prepare_chatlog(message_history: List[Message]) -> str:
    chatlog = ""
    for message in reversed(message_history):
        chatlog += f"\n{message.author.mention}: {message.content}"
    return chatlog


def convert_mentions_to_names(chatlog: str, name_mention_mapping: NameMentionMapping) -> str:
    output = re.sub(r"<@!?\d{18}>", lambda match: name_mention_mapping.get_name(match.group(0)), chatlog)
    return output


def convert_names_to_mentions(chatlog: str, name_mention_mapping: NameMentionMapping) -> str:
    regex = r"(" + r"|".join(name_mention_mapping.list_names()) + r")"
    output = re.sub(regex, lambda match: name_mention_mapping.get_mention(match.group(0)), chatlog)
    return output


def create_name_mention_mapping_from_history(message_history: List[Message]) -> NameMentionMapping:
    names = []
    mentions = []
    for message in message_history:
        message.mentions = cast(List[Member], message.mentions)
        for mention in message.mentions:
            for mention_form in _get_all_mention_forms(mention.mention):
                names.append("@" + mention.display_name)
                mentions.append(mention_form)
        for mention_form in _get_all_mention_forms(message.author.mention):
            names.append("@" + message.author.display_name)
            mentions.append(mention_form)
    return NameMentionMapping(names, mentions)


def _get_all_mention_forms(mention: str) -> List[str]:
    without_exclamation = mention.replace("!", "")
    return [without_exclamation, without_exclamation[:2] + "!" + without_exclamation[2:]]
