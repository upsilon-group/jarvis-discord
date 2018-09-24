import datetime
import logging
import re
from typing import List

import discord
from discord.ext import commands
from jarvis_discord import utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Moderation:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def check_message(self, list: List[str], message: discord.Message) -> bool:
        for stop_word in list:
            if stop_word in message.content.split():
                return True
        return False

    def blacklist(self, message: discord.Message) -> bool:
        with open("jarvis_discord/blacklist.txt", "r") as blacklist_file:
            blacklist_text = blacklist_file.read()
        blacklist = blacklist_text.splitlines()
        result = self.check_message(blacklist, message)
        return result

    async def blacklisted_message(self, message: discord.Message) -> None:
        if self.blacklist(message):
            if not isinstance(message.channel, discord.abc.PrivateChannel):
                await message.delete()
                await utils.self_delete(
                    message.channel, ":x: respecte les autres pour être respecté"
                )


def setup(bot: commands.Bot) -> None:
    moderation = Moderation(bot)
    bot.add_listener(moderation.blacklisted_message, "on_message")
    bot.add_cog(moderation)
