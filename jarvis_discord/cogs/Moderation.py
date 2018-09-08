import datetime
import logging

import discord
from discord.ext import commands
from jarvis_discord import utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Moderation:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def blacklist_check(self, message: discord.Message) -> bool:
        with open("jarvis_discord/blacklist.txt", "r") as blacklist_file:
            blacklist_text = blacklist_file.read()
        blacklist = blacklist_text.splitlines()
        for stop_word in blacklist:
            if message.content.find(stop_word) is not -1:
                return True
        return False

    async def blacklisted_message(self, message: discord.Message) -> None:
        if self.blacklist_check(message):
            if not isinstance(message.channel, discord.abc.PrivateChannel):
                await message.delete()
                await utils.self_delete(
                    message.channel, ":x: respecte les autres pour être respecté"
                )


def setup(bot: commands.Bot) -> None:
    moderation = Moderation(bot)
    bot.add_listener(moderation.blacklisted_message, "on_message")
    bot.add_cog(moderation)
