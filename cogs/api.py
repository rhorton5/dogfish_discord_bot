import discord, requests
from discord.ext import commands
from discord.ext.tasks import loop
from time import time, sleep

client = commands.Bot(command_prefix="$")

class API(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.insultQueue = []
        self.cheapSharkQueue = []
        self.foxxoQueue = []
        self.insultRequestQueue.start()
        self.foxxoRequestQueue.start()

    
    @loop(count=None,seconds=1.0)
    async def insultRequestQueue(self):
        if(len(self.insultQueue) != 0):
            json = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json").json()
            await self.insultQueue.pop(0).send(json["insult"])
    
    @loop(count=None,seconds=1.0)
    async def cheapSharkRequestQueue(self):
        if(len(self.cheapSharkQueue) != 0):
            print("Do something... this is stubbed for the time being")


    @client.command(help="Get personally insulted by Wrax.",alias=["roast"])
    async def insult(self,ctx):
        self.insultQueue.append(ctx)    

    @loop(count=None,seconds=1.0)
    async def foxxoRequestQueue(self):
        if(len(self.foxxoQueue) != 0):
            json = requests.get('https://randomfox.ca/floof/').json()
            await self.foxxoQueue.pop(0).send(json['image'])

    
    @client.command(help="Sends a picture of foxxos.",alias=["fox"])
    async def foxxo(self,ctx):
        self.foxxoQueue.append(ctx)



def setup(client):
    client.add_cog(API(client))
    