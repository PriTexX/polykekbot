import discord
from discord.ext import commands
import os


def main(TOKEN):
    intents = discord.Intents.default()

    intents.emojis = True
    intents.integrations = False
    intents.webhooks = False
    intents.dm_reactions = True
    intents.guild_reactions = True
    intents.presences = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command()
    async def load(ctx, extensions):
        bot.load_extension(f"cogs.{extensions}")
        await ctx.author.send("Done")

    @bot.command()
    async def unload(ctx, extensions):
        bot.unload_extension(f"cogs.{extensions}")
        await ctx.author.send("Done")

    @bot.command()
    async def reload(ctx, extensions):
        bot.unload_extension(f"cogs.{extensions}")
        bot.load_extension(f"cogs.{extensions}")
        await ctx.author.send("Done")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    bot.run(TOKEN)
if __name__ == '__main__':
    os.environ.__setitem__("token", "ODc5OTI1MDcwNjc4NjA5OTQx.YSW0FQ.GlDVrr51BrdmhxINi6yZZ7Gzw9g")
    _TOKEN = os.environ.get("token")
    main(_TOKEN)




