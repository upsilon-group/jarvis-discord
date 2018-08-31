import json
import logging
import sys
from typing import List, Optional

import discord
from jarvis_discord import exception

LOGGER = logging.getLogger(f"jarvis.{__name__}")


class Config:
    def __init__(self, fp: str) -> None:
        self.config_fp = fp
        try:
            with open(self.config_fp) as config_file:
                self.config = json.load(config_file)
            self._allow_dm = bool(self.config["allow_dm"])
            self._prefix = self.config["prefix"]
            self.default_cogs = self.config["default_cogs"]
            self.server = None
            self.server_name = self.config["server_name"]
            self._brawlhalla_token = self.config["api"]["brawlhalla"]["token"]
        except Exception as error:
            LOGGER.critical(f"JSON load '{self.config_fp}' failed: {error}")
            sys.exit()

    def token(self) -> str:
        try:
            token = self.config["token"]
            return token
        except Exception as error:
            LOGGER.critical(
                f"Unable to retrieve bot token: specify a bot token in -> {self.config_fp}: {error}"
            )
            sys.exit()

    def allow_dm(self) -> bool:
        return self._allow_dm

    def prefix(self) -> List[str]:
        try:
            if not self._prefix:
                raise exception.NoPrefix(
                    "No valid prefix: change it in {}".format(self.config_fp)
                )
            return self._prefix
        except exception.NoPrefix as error:
            LOGGER.critical(error)
            sys.exit()

    def base_cogs(self) -> List[str]:
        return self.default_cogs

    def guild(self, client: discord.Client) -> discord.Guild:
        self.server = discord.utils.get(client.guilds, name=self.server_name)
        if self.server is None:
            if len(client.guilds) == 1:
                self.server = client.guilds[0]
                return self.server
            LOGGER.critical(
                f"Unable to retrieve main server: specify a server name in -> {self.config_fp}"
            )
            sys.exit()
        return self.server

    def caps_max_percentage(self) -> int:
        try:
            caps_max_percentage = self.config["caps_max_percentage"]
            if caps_max_percentage in range(0, 101):
                return caps_max_percentage
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        caps_max_percentage = 101
        LOGGER.warning(
            f"Max caps percentage incorrect in '{self.config_fp}' -> Set to: no restriction."
        )
        return caps_max_percentage

    def caps_min_length(self) -> int:
        try:
            caps_min_length = self.config["caps_min_length"]
            if caps_min_length in range(0, 2001):
                return caps_min_length
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        caps_min_length = 2001
        LOGGER.warning(
            f"Min caps length incorrect in '{self.config_fp}' -> Set to: no restriction."
        )
        return caps_min_length

    def word_blacklist(self) -> List[str]:
        try:
            word_blacklist_fp = self.config["word_blacklist_fp"]
            with open(word_blacklist_fp) as word_blacklist_file:
                word_blacklist = word_blacklist_file.read().split()
                return word_blacklist
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        LOGGER.warning(
            f"Word blacklist incorrect in '{self.config_fp}' -> Set to: no restriction."
        )
        return []

    def channels_cmd(self) -> List[discord.TextChannel]:
        channels_cmd = []
        try:
            channels_cmd_names = self.config["channels"]["command"]
            for channel_cmd_name in channels_cmd_names:
                channel_cmd = discord.utils.get(
                    self.server.text_channels, name=channel_cmd_name
                )
                if channel_cmd is not None:
                    channels_cmd.append(channel_cmd)
                else:
                    LOGGER.error(
                        f"'{channel_cmd_name}' doesn't exist in '{self.server_name}'."
                    )
            if channels_cmd:
                return channels_cmd
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        channels_cmd = self.server.text_channels
        if not channels_cmd and not self._allow_dm:
            LOGGER.critical(
                f"Unable to retrieve command channels: specify one in -> {self.config_fp}"
            )
            sys.exit()
        if channels_cmd:
            LOGGER.warning("No valid commands channel -> set to 'all channels'.")
            return channels_cmd
        LOGGER.warning("No valid commands channel -> set to 'dm only'.")
        return channels_cmd

    def channel_report(self) -> Optional[discord.TextChannel]:
        try:
            channel_report_name = self.config["channels"]["report"]
            channel_report = discord.utils.get(
                self.server.text_channels, name=channel_report_name
            )
            if channel_report:
                return channel_report
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        LOGGER.warning("No valid report channel -> set to 'None'.")
        return None

    def channels_ignored(self) -> List[discord.TextChannel]:
        channels_ignored = []
        try:
            channels_ignored_names = self.config["channels"]["ignored"]
            for channel_ignored_name in channels_ignored_names:
                channel_ignored = discord.utils.get(
                    self.server.text_channels, name=channel_ignored_name
                )
                if channel_ignored is not None:
                    channels_ignored.append(channel_ignored)
                LOGGER.error(
                    f"'{channel_ignored_name}' doesn't exist in '{self.server_name}'."
                )
            if channels_ignored:
                return channels_ignored
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        LOGGER.warning("No valid ignored channel -> set to 'None'.")
        return channels_ignored

    def default_role(self) -> Optional[discord.Role]:
        try:
            default_role_name = self.config["default_role"]
            default_role = discord.utils.get(self.server.roles, name=default_role_name)
            if default_role:
                return default_role
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        LOGGER.warning("No valid default role -> set to 'None'.")
        return None

    def brawlhalla_token(self) -> Optional[str]:
        try:
            if self._brawlhalla_token:
                return self._brawlhalla_token
        except Exception as error:
            LOGGER.error(f"Reading config file '{self.config_fp}' failed: '{error}'.")
        LOGGER.warning("No valid brawlhalla token -> set to 'None'.")
        return None

    def brawlhalla_img_path(self) -> Optional[str]:
        if self._brawlhalla_token:
            try:
                brawlhalla_img_path = self.config["api"]["brawlhalla"]["image_url"]
                if brawlhalla_img_path:
                    return brawlhalla_img_path
            except Exception as error:
                LOGGER.error(
                    f"Reading config file '{self.config_fp}' failed: '{error}'."
                )
            LOGGER.warning("No valid brawlhalla images path -> set to 'None'.")
        return None
