import logging
import os
from typing import List

from discord import Message

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

LOG = logging.getLogger(__name__)


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
