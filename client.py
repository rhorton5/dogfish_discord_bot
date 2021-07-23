import discord, logging, help, sqlite3, json
from discord.ext.commands.errors import CheckFailure, CommandNotFound
from discord.ext import commands
from discord.ext.tasks import loop
from os import listdir
from random import choice

file = open("config.json","r")
config = json.load(file)
file.close()

async def getPrefix(bot,message):
    if message.guild == None:
        return "$"
    guild_id = message.guild.id
    db = sqlite3.connect(config['database_name'])
    cursor = db.cursor()
    cursor.execute('''select prefix from Guild where guild_id = ?''',(guild_id,))
    prefix = cursor.fetchone()[0]
    db.close()
    return prefix

bot = commands.Bot(command_prefix=getPrefix,help_command=help.Help(),intents=discord.Intents.all())

@bot.check
async def is_not_muted_channel(ctx):
    if ctx.guild == None: #DM Channels are excluded from this.
        return True
    channel_id, guild_id = ctx.channel.id, ctx.guild.id
    db = sqlite3.connect(config['database_name'])
    cursor = db.cursor()
    cursor.execute('''select muted_channels_ids from Guild where guild_id = ?''',(guild_id,))
    raw_channel_list = cursor.fetchone()[0]
    muted_channel_list = [int(muted_channel_id) for muted_channel_id in raw_channel_list.split(",")] if raw_channel_list != None else None #Muted_channels_ids should be listed as <id>, <id>... in the database.
    if muted_channel_list == None:
        return True
    elif channel_id in muted_channel_list:
        dmChannel = ctx.author.dm_channel
        if dmChannel == None:
            dmChannel = await ctx.author.create_dm()
        await dmChannel.send(f"Error: {ctx.channel.name} is apart of a muted channel for {ctx.guild.name}.")
        raise CheckFailure(f"Context is apart of {ctx.guild.name}'s muted channel: {ctx.channel.name}.")
        
    else:
        return channel_id not in muted_channel_list

@bot.event
async def on_ready():
    print("{0} is logged in!".format("Wrax"))
    
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong!\nLatency: **{round((bot.latency) * 1000,4)}** ms")

@loop(minutes=30,count=None)
async def changePresence():
    await bot.change_presence(activity=discord.Game(choice(config["presence_status"])))

@changePresence.before_loop
async def beforeChangePresence():
    await bot.wait_until_ready()

for filename in listdir("./cogs"):
    if filename.endswith('.py'):
        print(filename)
        bot.load_extension(f'cogs.{filename[:-3]}')

log = logging.getLogger('discord')
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)      

changePresence.start()
bot.run(config['token'])
