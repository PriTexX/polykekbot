import discord
from discord.ext import commands
import asyncio


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 2)


def setup(bot):
    bot.add_cog(Commands(bot))
