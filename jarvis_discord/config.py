"""Jarvis Discord BOT.

AUTHOR : Luoskate
VERSION : 1.1
"""
import json
from typing import Dict


class Config:
    # TODO: Add doc
    def __init__(self) -> None:
        self.config = self.load()

    def load(self) -> Dict:
        # TODO: Add doc
        with open("jarvis_discord/config.json") as config_file:
            return json.load(config_file)
