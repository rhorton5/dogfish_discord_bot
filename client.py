import discord, logging, help
from discord.ext import commands
from os import listdir
   
bot = commands.Bot(command_prefix='$',help_command=help.Help(),intents=discord.Intents.all())

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

log = logging.getLogger('discord')
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)      

bot.run('ODAxNjcwMzgwNjUzMjQ4NTky.YAkDuQ.qLLyUG9rPeZgpRZ5Di8ziY31OIU')
