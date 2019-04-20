"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import os
from typing import Dict, List

import discord
from discord.ext import commands

import jarvis_discord as jarvis
from jarvis_discord import utils

CONFIG = jarvis.Config()


class Jarvis(commands.Cog):
    # TODO: Add doc
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    async def extention_main(
        self, ctx: commands.Context, cogs: str, load: bool
    ) -> None:
        # TODO: Add doc
        cog_name = cogs.strip(",").lower()
        result: Dict[str, List[str]] = {"success": [], "failed": []}
        for cog in os.listdir("jarvis_discord/cogs"):
            if (
                cog_name != "jarvis.py"
                and (cog_name == "all" or cog[:-3] in cog_name)
                and cog.endswith(".py")
            ):
                state = utils.load_cog(self.bot, cog, load)
                if state:
                    result["success"].append(cog)
                else:
                    result["failed"].append(cog)

        embed = jarvis.ExtentionEmbed(ctx, result, load)
        await ctx.author.send(embed=embed)

    @commands.group(aliases=["cog", "ext"])
    @utils.check_cmd_role("extention")
    async def extention(self, ctx: commands.Context) -> None:
        # TODO: Add doc
        pass

    @extention.command()
    async def load(self, ctx: commands.Context, *, cogs: str) -> None:
        # TODO: Add doc
        async with ctx.author.typing():
            await self.extention_main(ctx, cogs, True)

    @extention.command()
    async def unload(self, ctx: commands.Context, *, cogs: str) -> None:
        # TODO: Add doc
        async with ctx.author.typing():
            await self.extention_main(ctx, cogs, False)

    @commands.group(name="bot", aliases=["jarvis"])
    async def jarvis_command(self, ctx: commands.Context) -> None:
        # TODO: Add doc
        pass

    @jarvis_command.command()
    @utils.check_cmd_role("bot.message")
    async def message(self, ctx, channel: discord.TextChannel, *, message: str) -> None:
        # TODO: Add doc
        # TODO: debug
        await channel.send(content=message)

    @jarvis_command.command()
    @utils.check_cmd_role("bot.disable")
    async def disable(self, ctx, disable_cmd: str) -> None:
        # TODO: Add doc
        enabled_commands = utils.get_subcommands(
            [cmd for cmd in self.bot.commands if cmd.enabled]
        )
        for command in enabled_commands:
            if disable_cmd == command.name:
                command.enabled = False
                await ctx.author.send(f"`{disable_cmd}` désactivé avec succès.")
                break
        else:
            await ctx.author.send(
                f"`{disable_cmd}` est déjà désactivé et/ou est introuvable."
            )

    @jarvis_command.command()
    @utils.check_cmd_role("bot.enable")
    async def enable(self, ctx, enable_cmd: str) -> None:
        # TODO: Add doc
        disabled_commands = utils.get_subcommands(
            [cmd for cmd in self.bot.commands if not cmd.enabled]
        )
        for command in disabled_commands:
            if enable_cmd == command.name:
                command.enabled = True
                await ctx.author.send(f"`{enable_cmd}` activé avec succès.")
                break
        else:
            await ctx.author.send(
                f"`{enable_cmd}` est déjà activé et/ou est introuvable."
            )

    @extention.error
    async def extention_error(self, ctx, error):
        # TODO: Add doc
        print(error)

    @jarvis_command.error
    async def jarvis_command_error(self, ctx, error):
        # TODO: Add doc
        print(error)

    @message.error
    async def message_error(self, ctx, error):
        # TODO: Add doc
        if isinstance(error, commands.BadArgument):
            await ctx.author.send(
                f"Je suis désolé je n'ai pas trouvé : `{' '.join(ctx.message.content.split()[1:])}`."
            )

    # TODO: Add reaction support
    # TODO: Add embed support


def setup(bot: discord.Client) -> None:
    # TODO: Add doc
    bot.add_cog(Jarvis(bot))
