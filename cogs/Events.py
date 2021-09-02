import discord
from discord.ext import commands
import asyncio


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = {
            '1️⃣': 876865896579235890,
            '2️⃣': 879001835569029150,
            '3️⃣': 879001839335538688,
            '4️⃣': 879001842510594078,
        }

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('...'))
        print("Ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = await member.send("Выбери свою касту")

        emojis = [emoji for emoji in self.roles.keys()]

        for emoji in emojis:
            await msg.add_reaction(emoji)

        def check(payload):
            return payload.emoji.name in emojis and payload.message_id == msg.id and payload.user_id != 879925070678609941

        try:
            payload = await self.bot.wait_for("raw_reaction_add", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await member.send("Слишком долго думал. Чтобы получить роль перейди в канал 'получение-роли'")
            role = discord.utils.get(member.guild.roles, id=882020283354054726)
            await member.add_role(role)
        else:
            role = discord.utils.get(member.guild.roles, id=self.roles[payload.emoji.name])
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 882637739705634846:
            for role_ in payload.member.roles:
                if role_.id in self.roles.values():
                    await payload.member.remove_roles(discord.utils.get(payload.member.guild.roles, id=role_.id))
            role = discord.utils.get(payload.member.guild.roles, id=self.roles[payload.emoji.name])
            await payload.member.add_roles(role)
            role_to_remove = discord.utils.get(payload.member.guild.roles, id=882020283354054726)
            await payload.member.remove_roles(role_to_remove)
            await payload.member.send("Роль выдана")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 882637739705634846:
            member = self.bot.guilds[0].get_member(payload.user_id)
            role_to_remove = discord.utils.get(self.bot.guilds[0].roles, id=self.roles[payload.emoji.name])

            if role_to_remove not in member.roles:
                return

            no_role = discord.utils.get(self.bot.guilds[0].roles, id=882020283354054726)
            await member.add_roles(no_role)
            await member.remove_roles(role_to_remove)


def setup(bot):
    bot.add_cog(Events(bot))
