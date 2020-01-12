import socket
from typing import Optional

import aiohttp
from discord.ext import commands


class Bot(commands.Bot):
    """A subclass of `discord.ext.commands.Bot` with an aiohttp session and an API client."""

    def __init__(self, *args, **kwargs):
        self.connector = aiohttp.TCPConnector(
            resolver=aiohttp.AsyncResolver(),
            family=socket.AF_INET,
        )

        super().__init__(*args, connector=self.connector, **kwargs)

        self.http_session: Optional[aiohttp.ClientSession] = None

    async def start(self, *args, **kwargs) -> None:
        """Open an aiohttp session before logging in and connecting to Discord."""
        self.http_session = aiohttp.ClientSession(connector=self.connector)

        await super().start(*args, **kwargs)
