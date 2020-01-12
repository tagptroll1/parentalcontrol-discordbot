from pathlib import Path

import discord
from discord.ext.commands import when_mentioned_or

from bot.bot import Bot
from bot.constants import Bot as BotConfig


bot = Bot(
    command_prefix=when_mentioned_or(BotConfig.prefix),
    activity=discord.Game(name=f"Commands: {BotConfig.prefix}help"),
    case_insensitive=True,
    max_messages=10_000,
)

cogs = Path("./bot/cogs")
for cog in cogs.iterdir():
    if cog.is_dir():
        continue

    if cog.suffix == ".py" and cog.stem != "__init__":
        path = ".".join(cog.with_suffix("").parts)
        try:
            bot.load_extension(path)
            print(f"{'Loaded...':<19} {path:<1}!")
        except Exception as e:
            print(f"{'Failed to load...':<19} {path:<1}!")
            print(e, "\n")

bot.run(BotConfig.token)
