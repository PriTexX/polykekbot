import discord
from discord.ext import commands
import asyncio


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):

        roles = {
            '1️⃣': 880488370252427275,
            '2️⃣': 880488599555014706,
            '3️⃣': 880488808263610479,
            '4️⃣': 880488932914114571,
        }

        emojis = [emoji for emoji in roles.keys()]
        message = await ctx.author.send("Выбери свою роль")

        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(payload):
            return payload.emoji.name in emojis and payload.message_id == message.id and payload.user_id != 879925070678609941

        try:
            payload = await self.bot.wait_for("raw_reaction_add", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.author.send("Для выбора роли напиши '!role' повторно")
        else:
            adminIDS = [229033111197843456, 249916623912173570]
            admins = []

            for id in adminIDS:
                admins.append(self.bot.get_user(id))

            for admin in admins:
                msg = await admin.send(f"Подтвердите роль {payload.emoji.name} у {ctx.author}")
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")

                member = discord.utils.get(self.bot.guilds[0].members, id=ctx.author.id)

                def check_admin(payload):
                    return payload.message_id==msg.id and payload.user_id in adminIDS

                try:
                    payload_admin = await self.bot.wait_for("raw_reaction_add", check=check_admin, timeout=360.0)
                except asyncio.TimeoutError:
                    await member.send("Админ ушел срать. Повторите запрос позже")
                else:
                    if payload_admin.emoji.name == "✅":
                        role = discord.utils.get(self.bot.guilds[0].roles, id=roles[payload.emoji.name])
                        await member.add_roles(role)
                        await member.send("Успешная смена роли")
                    else:
                        print(payload_admin.emoji.name)
                        print(payload_admin.emoji)
                        await member.send("Админ отклонил запрос на смену роли")

def setup(bot):
    bot.add_cog(Test(bot))
