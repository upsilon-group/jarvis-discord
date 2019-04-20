"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import asyncio
import locale
import logging
from typing import List, Optional

import discord
from discord.ext import commands

import jarvis_discord as jarvis
from jarvis_discord import utils

locale.setlocale(locale.LC_TIME, "")

FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] <%(name)s> - [%(funcName)s] - %(message)s", "%x %X"
)

# Logger for discord.py package

DISCORD_LOGGER = logging.getLogger("discord")
DISCORD_LOGGER.setLevel(logging.INFO)
DISCORD_HANDLER = logging.FileHandler(
    filename="logs/discord.log", encoding="utf-8", mode="w+"
)
DISCORD_HANDLER.setFormatter(FORMATTER)
DISCORD_LOGGER.addHandler(DISCORD_HANDLER)

# Logger for Jarvis

LOGGER = logging.getLogger("jarvis")
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.FileHandler(filename="logs/jarvis.log", encoding="utf-8", mode="w+")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

# Config var

CONFIG = jarvis.Config()
TOKEN = CONFIG.config["token"]


class Jarvis(commands.Bot):
    # TODO: Add doc
    """Bot object.

    A bit longer description.

    """

    async def on_ready(self) -> None:
        # TODO: Add doc
        """Load default cogs.

        A bit longer description.

        """
        LOGGER.info(f"Logged in as : {str(self.user)}, ID: {self.user.id}")
        utils.load_default_cogs(self)

    async def on_member_join(self, member: discord.Member) -> None:
        # TODO: Add doc
        """Add default role to new members.

        A bit longer description.

        Args:
            variable (type): description

        """
        guild = member.guild
        default_role = discord.utils.get(
            guild.roles, name=CONFIG.config["default_role"]
        )
        LOGGER.info(f"New Member ! : {str(member)}")
        if default_role:
            try:
                await member.add_roles(
                    default_role, reason="Default role for new member"
                )
                LOGGER.info(f"Added {default_role.name} role to {str(member)}")
            except discord.HTTPException:
                LOGGER.info(
                    f"{default_role.name} role doesn't exist in server : {guild.name}"
                )

    async def on_message_delete(self, message: discord.Message) -> None:
        # TODO: Add doc
        """Log deleted messages.

        A bit longer description.

        Args:
            variable (type): description

        """
        LOGGER.info(f"↪ message: {str(message.author)}: {message.content}")

    async def on_raw_message_delete(
        self, payload: discord.RawMessageDeleteEvent
    ) -> None:
        # TODO: Add doc
        """Log deleted messages.

        A bit longer description.

        Args:
            variable (type): description

        """
        channel = self.get_channel(payload.channel_id)
        if payload.guild_id:
            guild = self.get_guild(payload.guild_id)
            LOGGER.info(
                f"message ID: {payload.message_id} in #{channel.name} -> {guild.name}."
            )
        else:
            LOGGER.info(
                f"message ID: {payload.message_id} in {str(channel.recipient)}."
            )

    async def on_message_edit(
        self, message_before: discord.Message, message_after: discord.Message
    ) -> None:
        # TODO: Add doc
        """Log edited messages.

        A bit longer description.

        Args:
            variable (type): description
        """
        LOGGER.info(
            f"↪ message: {str(message_before.author)}: {message_before.content} ⟾ {str(message_after.author)}: {message_after.content}"
        )

    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent) -> None:
        # TODO: Add doc
        """Log edited messages.

        A bit longer description.

        Args:
            variable (type): description

        """
        if payload.data["embeds"] != []:
            channel = self.get_channel(int(payload.data["channel_id"]))
            message = await channel.fetch_message(payload.message_id)
            LOGGER.info(
                f"{payload.message_id} in {str(channel.recipient) if isinstance(channel, discord.DMChannel) else channel.name}"
            )
            await self.on_message(message, log=False)

    async def on_message(self, message: discord.Message, log: bool = True) -> None:
        # TODO: Add doc
        """Log and verify message.

        A bit longer description.

        Args:
            variable (type): description

        """
        channels_cmd: List[Optional[discord.TextChannel]] = []
        guild = message.guild
        if guild:
            for channel_cmd in CONFIG.config["channels"]["command"]:
                channels_cmd.append(discord.utils.get(guild.channels, name=channel_cmd))
        if log:
            LOGGER.info(
                f"{message.id} : in {str(message.channel.recipient) if isinstance(message.channel, discord.abc.PrivateChannel) else message.channel.name}"
            )
            LOGGER.info(f"↪ message: {str(message.author)}: {message.content}")
        if message.channel in channels_cmd:
            await message.delete()
        await self.process_commands(message)

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        # TODO: Add doc
        """Reply to error.

        A bit longer description.

        Args:
            variable (type): description

        """
        prefix = ctx.prefix.replace(ctx.bot.user.mention, f"@{ctx.bot.user.name}")
        if isinstance(error, commands.CommandNotFound):
            await ctx.author.send(f"Désolé mais cette commande n'existe pas encore.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send(
                f":x:**La commande est désactivé.**\n*Contactez un Administrateur pour plus d'information*"
            )
        elif isinstance(error, commands.CheckFailure):
            await ctx.author.send(
                f":x:**Vous n'avez pas la permission pour cette action**"
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(
                f":x:Désolé mais cette commande n'ait pas disponible en message privé."
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.author.send(
                f"Je ne peux pas deviner : `{error.param.name}`.\nUtilisez *{prefix}help {ctx.command.full_parent_name} {ctx.invoked_with}*"
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(
                f":x:Désolé mais cette commande est inutilisable temporairement.\nRéessayez dans `{error.retry_after}s`"
            )


# TODO: add error handler
BOT = Jarvis(
    command_prefix=utils.get_prefix,
    help_command=jarvis.JarvisHelpCommand(
        dm_help=True,
        commands_heading="Commandes :",
        no_category="Sans catégorie",
        command_attrs={"help": "Affiche ce message"},
    ),
)

LOOP = asyncio.get_event_loop()

try:
    # Start Jarvis
    LOOP.run_until_complete(BOT.start(TOKEN))
except discord.LoginFailure as err:
    print(err)
except KeyboardInterrupt:
    LOGGER.info("Exit : Keyboard Interrupt")
    print("Successfully exit")
finally:
    # Cancel all tasks lingering
    for task in asyncio.Task.all_tasks():
        task.cancel()
    # Logs out of Discord and close the loop
    LOOP.run_until_complete(BOT.logout())
    LOOP.close()
