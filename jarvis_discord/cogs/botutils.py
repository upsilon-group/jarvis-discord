import datetime
import logging
import os

import discord
from discord.ext import commands
from jarvis_discord import utils

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class BotUtils:
    """."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["modules"])
    async def module(self, ctx) -> None:
        if ctx.invoked_subcommand is None:
            pass

    @module.command()
    async def load(self, ctx, *, cogs):
        cog = cogs.strip(",")
        dict_result = {"result": "", "success": [], "failed": []}
        for module in os.listdir("jarvis_discord/cogs"):
            if module.endswith(".py") and module != "botutils.py":
                try:
                    if cog == "all" or module[:-3] in cog:
                        self.bot.unload_extension(f"jarvis_discord.cogs.{module[:-3]}")
                        self.bot.load_extension(f"jarvis_discord.cogs.{module[:-3]}")
                        LOGGER.info(f"Successfully load cog: <{module[:-3]}>.")
                        dict_result["success"].append(module)
                except Exception as error:
                    LOGGER.error(
                        f"Could not load module <{module}> due to {error.__class__.__name__}: {error}"
                    )
                    dict_result["failed"].append(module)
        dict_result[
            "result"
        ] = f"__***{len(dict_result['success'])}/{len(dict_result['success']) + len(dict_result['failed'])}***__ modules chargés."
        await utils.embed_msg(
            ctx.author,
            dict_result["result"],
            ctx.author.color.value
            if isinstance(ctx.channel, discord.abc.GuildChannel)
            else int("451E7E", 16),
            None,
            datetime.datetime.now(),
            None,
            self.bot.user.avatar_url,
            ctx.author.name,
            "https://discord.gg/nesNrkn",
            ctx.author.avatar_url,
            f"Use {ctx.prefix} help to get info !",
            self.bot.user.avatar_url,
            {
                "name": "Succés :",
                "value": dict_result["success"],
                "inline": False,
            },
            {
                "name": "Échecs :",
                "value": dict_result["failed"],
                "inline": False,
            },
        )

    @module.command()
    async def unload(self, ctx, *, cogs):
        cog = cogs.strip(",")
        dict_result = {"result": "", "success": [], "failed": []}
        for module in os.listdir("jarvis_discord/cogs"):
            if module.endswith(".py") and module != "botutils.py":
                try:
                    if cog == "all" or module[:-3] in cog:
                        self.bot.unload_extension(f"jarvis_discord.cogs.{module[:-3]}")
                        LOGGER.info(f"Successfully unload cog: {module[:-3]}.")
                        dict_result["success"].append(module)
                except Exception as error:
                    LOGGER.error(
                        f"Could not unload module {module} due to {error.__class__.__name__}: {error}"
                    )
                    dict_result["failed"].append(module)
        dict_result[
            "result"
        ] = f"__***{len(dict_result['success'])}/{len(dict_result['success']) + len(dict_result['failed'])}***__ modules déchargés."
        await utils.embed_msg(
            ctx.author,
            dict_result["result"],
            ctx.author.color.value
            if isinstance(ctx.channel, discord.abc.GuildChannel)
            else int("451E7E", 16),
            None,
            datetime.datetime.now(),
            None,
            self.bot.user.avatar_url,
            ctx.author.name,
            "https://discord.gg/nesNrkn",
            ctx.author.avatar_url,
            f"Use {ctx.prefix} help to get info !",
            self.bot.user.avatar_url,
            {
                "name": "Succés :",
                "value": dict_result["success"],
                "inline": False,
            },
            {
                "name": "Échecs :",
                "value": dict_result["failed"],
                "inline": False,
            },
        )


def setup(bot):
    bot.add_cog(BotUtils(bot))
