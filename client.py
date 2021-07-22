import discord, logging,help, sqlite3,json
from discord.ext import commands
from os import listdir

file = open("config.json","r")
config = json.load(file)
file.close()

async def getPrefix(bot,message):
    guild_id = message.guild.id
    db = sqlite3.connect(config['database_name'])
    cursor = db.cursor()
    cursor.execute('''select prefix from Guild where guild_id = ?''',(guild_id,))
    prefix = cursor.fetchone()[0]
    db.close()
    return prefix

bot = commands.Bot(command_prefix=getPrefix,help_command=help.Help(),intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("{0} is logged in!".format("Wrax"))
    
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong!\nLatency: {round((bot.latency) * 1000,4)} ms")



for filename in listdir("./cogs"):
    if filename.endswith('.py'):
        print(filename)
        bot.load_extension(f'cogs.{filename[:-3]}')
		#Status.py is causing duplicate commands to be sent.



log = logging.getLogger('discord')
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)      

bot.run(config['token'])
