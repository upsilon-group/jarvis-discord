import asyncio
import logging

import discord
from discord.ext import commands
from jarvis_discord import config, utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")
CONFIG = config.Config("jarvis_discord/config.json")


class Rainbow:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.discord_colors = discord.Colour.default()
        self.rainbow_running = True
        self.rainbow_task = None

    def set_rainbow(self) -> None:
        colors = [
            "FF0000",
            "FF003F",
            "FF007F",
            "FF00BF",
            "FF00FF",
            "BF00FF",
            "7F00FF",
            "3F00FF",
            "0000FF",
            "003FFF",
            "007FFF",
            "00BFFF",
            "00FFFF",
            "00FFBF",
            "00FF7F",
            "00FF3F",
            "00FF00",
            "3FFF00",
            "7FFF00",
            "BFFF00",
            "FFFF00",
            "FFBF00",
            "FF7F00",
            "FF3F00",
        ]
        self.discord_colors = [discord.Colour(int(color, 16)) for color in colors]

    @commands.command(aliases=["rnbw"])
    async def rainbow(self, ctx, *, value: str) -> None:
        if value.lower() == "true":
            self.rainbow_running = True
        elif value.lower() == "false":
            self.rainbow_running = False
        else:
            raise commands.BadArgument()

    @rainbow.error
    async def rainbow_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await utils.self_delete(ctx, f"{' '.join(str(ctx.args))} est incorrecte.")

    async def rainbow_loop(self) -> None:
        guild = CONFIG.guild(self.bot)
        rainbow_role = discord.utils.get(guild.roles, name="rainbow")
        while not self.bot.is_closed():
            if self.rainbow_running:
                for discord_color in self.discord_colors:
                    await rainbow_role.edit(color=discord_color)
                    await asyncio.sleep(0.3)

    def start(self) -> None:
        self.set_rainbow()
        loop = asyncio.get_event_loop()
        self.rainbow_task = loop.create_task(self.rainbow_loop())

    def close(self) -> None:
        self.rainbow_task.cancel()


def setup(bot: commands.Bot) -> None:
    rainbow = Rainbow(bot)
    rainbow.start()
    bot.add_cog(rainbow)


def teardown(bot: commands.Bot) -> None:
    print("tear")
    rainbow = Rainbow(bot)
    rainbow.close()
