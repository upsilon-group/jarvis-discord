"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import logging
from typing import List, Optional

import discord
from discord.ext import commands
from jarvis_discord import config, utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")
CONFIG = config.Config()


class Moderation(commands.Cog):
    # TODO: add doc
    def __init__(self, bot: commands.Bot) -> None:
        with open("jarvis_discord/blacklist.txt", "r") as blacklist_file:
            self.blacklist_text = blacklist_file.read()

        self.channels_ignored: List[Optional[discord.TextChannel]] = []
        for channel_ignored in CONFIG.config["channels"]["command"]:
            channel_ignored = discord.utils.get(
                bot.get_all_channels(), name=channel_ignored
            )
            if isinstance(channel_ignored, discord.TextChannel):
                self.channels_ignored.append(channel_ignored)

    def check_message(self, blacklist: List[str], message: discord.Message) -> bool:
        # TODO: add doc
        for stop_word in blacklist:
            if stop_word in message.content.split():
                return True
        return False

    def blacklist(self, message: discord.Message) -> bool:
        # TODO: add doc
        blacklist = self.blacklist_text.splitlines()
        result = self.check_message(blacklist, message)
        return result

    async def blacklisted_message(self, message: discord.Message) -> None:
        # TODO: add doc
        if self.blacklist(message):
            if (
                isinstance(message.channel, discord.abc.GuildChannel)
                and message.channel not in self.channels_ignored
            ):
                await message.delete()
                await utils.self_delete(message.channel, ":x: parle autrement.")


def setup(bot: commands.Bot) -> None:
    # TODO: add doc
    moderation = Moderation(bot)
    bot.add_listener(moderation.blacklisted_message, "on_message")
    bot.add_cog(moderation)
