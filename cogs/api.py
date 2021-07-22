import discord, requests, typing
from discord.ext import commands
from discord.ext.tasks import loop
from time import time, sleep

class API(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.insultQueue = []
        self.cheapSharkQueue = []
        self.foxxoQueue = []
        self.doggoQueue = []
        self.insultRequestQueue.start()
        self.foxxoRequestQueue.start()
        self.doggoRequestQueue.start()

    
    @loop(count=None,seconds=1.0)
    async def insultRequestQueue(self):
        if(len(self.insultQueue) != 0):
            json = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json").json()
            await self.insultQueue.pop(0).send(json["insult"])
    
    @loop(count=None,seconds=1.0)
    async def cheapSharkRequestQueue(self):
        if(len(self.cheapSharkQueue) != 0):
            print("Do something... this is stubbed for the time being")


    @commands.command(help="Get personally insulted by Wrax.",alias=["roast"])
    async def insult(self,ctx):
        self.insultQueue.append(ctx)    

    @loop(count=None,seconds=1.0)
    async def foxxoRequestQueue(self):
        if(len(self.foxxoQueue) != 0):
            json = requests.get('https://randomfox.ca/floof/').json()
            await self.foxxoQueue.pop(0).send(json['image'])


    @loop(count=None,seconds=1.0)
    async def doggoRequestQueue(self):
        if(len(self.doggoQueue) != 0):
            data = self.doggoQueue.pop(0)
            ctx = data['context']
            if data['breed'] == None:
                json = requests.get('https://dog.ceo/api/breeds/image/random').json()
            else:
                json = requests.get('https://dog.ceo/api/breed/{}/images/random'.format(data['breed'].lower())).json()
            if json['status'] == "success":
                await ctx.send(json['message'])
            else:
                await ctx.send(f"An error has occured...\n {json['message']}")

    
    @commands.command(help="Sends a picture of foxxos.",alias=["fox"])
    async def foxxo(self,ctx):
        self.foxxoQueue.append(ctx)
    
    @commands.command(help="Sends a picture of a doggo.",alias=["dog"])
    async def doggo(self,ctx,*,breed: typing.Optional[str] = None):
        self.doggoQueue.append({"context": ctx, "breed": breed})    

def setup(client):
    client.add_cog(API(client))
