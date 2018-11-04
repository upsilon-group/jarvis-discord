import datetime
import logging
import re
from typing import List

import discord
from discord.ext import commands
from jarvis_discord import config, utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")
CONFIG = config.Config("jarvis_discord/config.json")


class Moderation:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        guild = CONFIG.guild(self.bot)
        self.channels_ignored = CONFIG.channels_ignored()

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
            if (
                isinstance(message.channel, discord.abc.GuildChannel)
                and message.channel not in self.channels_ignored
            ):
                await message.delete()
                await utils.self_delete(message.channel, ":x: parle autrement.")


def setup(bot: commands.Bot) -> None:
    moderation = Moderation(bot)
    bot.add_listener(moderation.blacklisted_message, "on_message")
    bot.add_cog(moderation)
