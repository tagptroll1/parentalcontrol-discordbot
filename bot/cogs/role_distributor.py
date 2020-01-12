from discord import Embed, Member, RawReactionActionEvent, Role
from discord.ext import commands

from bot.constants import Channels, Emojis, Guild, People, Roles


class RoleDistributor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.guild = None
        self.welcome_channel = None
        self.log_channel = None

        self.roles = {
            "druid": Roles.druid,
            "hunter": Roles.hunter,
            "mage": Roles.mage,
            "paladin": Roles.paladin,
            "priest": Roles.priest,
            "rogue": Roles.rogue,
            "warlock": Roles.warlock,
            "warrior": Roles.warrior,
        }

        self.emojis = {
            "warrior": Emojis.warrior,
            "warlock": Emojis.warlock,
            "rogue": Emojis.rogue,
            "priest": Emojis.priest,
            "paladin": Emojis.paladin,
            "mage": Emojis.mage,
            "hunter": Emojis.hunter,
            "druid": Emojis.druid,
        }

    async def ensure_variables(self):
        if not self.guild:
            self.guild = self.bot.get_guild(Guild.id)
            if not self.guild:
                self.guild = await self.bot.fetch_guild(Guild.id)

        if not self.welcome_channel:
            self.welcome_channel = self.bot.get_channel(Channels.welcome)
            if not self.welcome_channel:
                self.welcome_channel = await self.bot.fetch_channel(Channels.welcome)

        if not self.log_channel:
            self.log_channel = self.bot.get_channel(Channels.log)
            if not self.log_channel:
                self.log_channel = await self.bot.fetch_channel(Channels.log)

    async def log_adding_role(self, member: Member, role: Role):
        embed = Embed()
        embed.description = f"Added the role {role} to {member.display_name}"
        embed.color = 0x68c290

        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.ensure_variables()

        # ignore owner
        if payload.user_id == People.owner:
            return

        emoji = payload.emoji
        message_id = payload.message_id

        # Find the role they clicked on based on emoji str
        for key, value in self.emojis.items():
            if str(emoji) == value:
                role_id = self.roles.get(key)

                if not role_id:
                    return

                break
        # If loop finishes it didn't find it
        else:
            return

        # Check it's the right message (any in welcome channel posted by an officer)
        try:
            message = await self.welcome_channel.fetch_message(message_id)
            author = message.author

            if not any(role.id == Roles.officer for role in author.roles):
                return
        except Exception as e:
            return

        member = self.guild.get_member(payload.user_id)

        if not member:
            member = self.guild.fetch_member(payload.user_id)

        for role in member.roles:
            if role.id in self.roles.values():
                await message.remove_reaction(emoji, member)
                await member.send(f"You already a {role}! Contact a moderator to change it.")
                return

        role = self.guild.get_role(role_id)
        try:
            await member.add_roles(role, reason="Added class role")
            print(f"Added the {role} role to {member.display_name}")
            await self.log_adding_role(member, role)
        finally:
            await message.remove_reaction(emoji, member)


def setup(bot: commands.Bot) -> None:
    """Load the Alias cog."""
    bot.add_cog(RoleDistributor(bot))
