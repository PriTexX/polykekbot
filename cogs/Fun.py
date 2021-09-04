import discord
from discord.ext import commands
import json


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def petuh(self, ctx, member: discord.Member):
        with open('cogs/data.json', 'r') as file:
            takenRoles = json.load(file)
        roles_to_take = [role.name for role in member.roles]
        takenRoles[member.name] = roles_to_take
        with open('cogs/data.json', 'w') as file:
            json.dump(takenRoles, file)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='ПЕТУШАРНЯ')
        await member.add_roles(mute_role)
        for i in range(1, len(roles_to_take)):
            await member.remove_roles(discord.utils.get(ctx.message.guild.roles, name=roles_to_take[i]))
        await member.move_to(None)
        await ctx.send(f'{member.mention} был лишен всех прав и отправлен в ПЕТУШАРНЮ')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unpetuh(self, ctx, member: discord.Member):
        with open('cogs/data.json', 'r') as file:
            takenRoles = json.load(file)
        remove_role = discord.utils.get(ctx.message.guild.roles, name='ПЕТУШАРНЯ')
        await member.remove_roles(remove_role)
        roles_to_give = takenRoles[member.name]
        for role in range(1, len(roles_to_give)):
            await member.add_roles(discord.utils.get(ctx.message.guild.roles, name=roles_to_give[role]))
        await ctx.send(f'{ctx.author.mention} вытащил {member.mention} из ПЕТУШАРНИ и вернул все права')


def setup(bot):
    bot.add_cog(Fun(bot))