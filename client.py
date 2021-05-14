import discord
import traceback
from discord.ext import commands
from discord.ext.commands.converter import MemberConverter, MessageConverter
from commandScripts import changeColor
import commandScripts.help
from os import listdir
   
bot = commands.Bot(command_prefix='!',help_command=commandScripts.help.Help(),intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("{0} is logged in!".format("Wrax"))

@bot.event
async def on_message(message):
    print("{0.author}: {0.content}".format(message))
    

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")



for filename in listdir("./cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
            
bot.run('ODAxNjcwMzgwNjUzMjQ4NTky.YAkDuQ.qLLyUG9rPeZgpRZ5Di8ziY31OIU')
