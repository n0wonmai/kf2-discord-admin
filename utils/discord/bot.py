from discord.ext import commands
from utils.discord.ui import UserMenu
from utils.webadmin.webadmin import server_info
from utils.toolbox import read_config

import os
import discord
import logging

log = logging.getLogger("kf2bot")

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.json")

def bot_run():
    """ Bot Settings """

    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game('!info')
        )

    """
    Bot commands:

    - !info (displays bot info)

    - !status (displays current server status)
    """

    @commands.command()
    async def info(ctx):
        """ !info command """

        log.info(f"Command !info requested by {ctx.author.name}")

        # Embed ini
        emb = discord.Embed(title='📌  Bot commands', colour=discord.Color.dark_purple(), url='')
        emb.set_footer(text = f"Requested by: {ctx.author.name}", icon_url = ctx.author.avatar)
        emb.set_image(url = read_config(PATH)["poster_url"])

        # Additional fields
        emb.add_field(name='❓  !info', value = 'Displays bot info')
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name='🚀  !status', value = 'Displays current server status')
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name = chr(173), value = chr(173))

        await ctx.send(embed = emb)


    @commands.command()
    async def status(ctx):
        """ !status command """

        status = await server_info()
        log.info(f"Command !status requested by {ctx.author.name}")

        # Embed ini
        emb = discord.Embed(title='📊  Server status', colour=discord.Color.dark_purple(), url='')
        emb.set_footer(text = f"Requested by: {ctx.author.name}", icon_url = ctx.author.avatar)

        # Additional fields
        emb.add_field(name='Map:', value = status["map"])
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name='Wave:', value = status["wave"])
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name = chr(173), value = chr(173))
        ## Optional: get difficulty
        # emb.add_field(name='Difficulty:', value = status["difficulty"])
        # emb.add_field(name = chr(173), value = chr(173))
        # emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name='Players:', value = status["players"])
        emb.add_field(name = chr(173), value = chr(173))
        emb.add_field(name = chr(173), value = chr(173))

        menu = UserMenu()
        await ctx.send(embed = emb, view = menu)


    # Add commands to bot
    bot.add_command(info)
    bot.add_command(status)

    # Bot authorization
    bot.run(read_config(PATH)["bot_token"])


if __name__ == "__main__":
    pass
