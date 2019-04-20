"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import logging
import os
from typing import List, Optional

import discord
from discord.ext import commands

import jarvis_discord as jarvis

LOGGER = logging.getLogger(f"jarvis.{__name__}")

CONFIG = jarvis.Config()
PREFIX = CONFIG.config["prefix"]
DEFAULT_COGS = CONFIG.config["default_cogs"]


class JarvisHelpCommand(commands.DefaultHelpCommand):
    def command_not_found(self, string):
        return 'Aucune commande nommé "{}" n\'a été trouvé.'.format(string)

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and command.all_commands:
            return 'La commande "{0.qualified_name}" n\'a pas de sous-commande nommé "{1}"'.format(
                command, string
            )
        return 'La commande "{0.qualified_name}" n\'a pas de sous-commande'.format(
            command
        )

    def get_ending_note(self):
        command_name = self.invoked_with
        return (
            "Tapez {0}{1} [commande] pour plus d'infos sur une commande.\n"
            "Vous pouvez aussi taper {0}{1} [catégorie] pour plus d'infos sur une catégorie.".format(
                self.clean_prefix, command_name
            )
        )


def trans_activity(activity):
    activities = {
        "playing": "Joue à ",
        "streaming": "Stream ",
        "listening": "Écoute ",
        "watching": "Regarde ",
    }
    return activities[str(activity.type)[13:]]


def trans_status(status):
    statuts = {
        "online": "En ligne",
        "idle": "Absent",
        "dnd": "Ne pas déranger",
        "offline": "déconnecté",
    }
    return statuts[str(status)]


def check_cmd_role(roles_str):
    def predicate(ctx):
        for role in (
            ctx.bot.get_guild(CONFIG.config["guild_id"]).get_member(ctx.author.id).roles
        ):
            if role.name in CONFIG.config["role_permission"]["commands"][roles_str]:
                return True
        return False

    return commands.check(predicate)


async def self_delete(channel: discord.abc.Messageable, *args: str) -> None:
    # TODO: Add doc
    for arg in args:
        await channel.send(content=arg, delete_after=4)


def get_prefix(self, message):
    # TODO: Add doc
    prefix = commands.when_mentioned(self, message)
    for pre in PREFIX:
        prefix.append(pre)
    return prefix


def get_subcommands(_commands: List[commands.command]) -> List[commands.command]:
    # TODO: Add doc
    check_commands = _commands.copy()
    while check_commands:
        subcommands: List[Optional[commands.command]] = []
        for command in check_commands:
            try:
                subcommands.extend(command.commands)
                _commands.extend(command.commands)
            except Exception:
                pass
        check_commands = subcommands.copy()
    return _commands


def load_cog(bot: discord.Client, cog: str, load: bool) -> bool:
    # TODO: Add doc
    try:
        if load:
            bot.reload_extension(f"jarvis_discord.cogs.{cog[:-3]}")
        else:
            bot.unload_extension(f"jarvis_discord.cogs.{cog[:-3]}")
    except commands.ExtensionNotLoaded:
        if load:
            bot.load_extension(f"jarvis_discord.cogs.{cog[:-3]}")
    except Exception as error:
        LOGGER.error(
            f"Could not {'load' if load else 'unload'} module <{cog}> due to {error.__class__.__name__}: {error}"
        )
        return False
    LOGGER.info(f"Successfully {'load' if load else 'unload'} cog: <{cog[:-3]}>.")
    return True


def load_default_cogs(bot: discord.Client) -> None:
    # TODO: Add doc
    for cog in os.listdir("jarvis_discord/cogs"):
        if cog in DEFAULT_COGS:
            load_cog(bot, cog, True)
