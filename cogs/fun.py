import discord
from discord.ext import commands
from random import choice, randint

client = commands.Bot(command_prefix="$")

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Cog is ready!")
    
    @client.command(help="Reverses your message.",aliases=["backwards","reverseMessage","reverse_message"])
    async def reverse(self,ctx,*,content):
        await ctx.send(content[::-1])
    
    @client.command(help="Poke and annoy another member on your server.  This is chosen at random.")
    async def poke(self,ctx):
        target = choice([member for member in await ctx.guild.fetch_members().flatten() if member.bot is False])
        if target.name == ctx.author.name:
            await ctx.send("You've poked yourself")
        else:
            await ctx.send("{} has been poked by {}!".format(target.mention,ctx.author.name))  
    
    @client.command(help="Kill a member on the server; however, they might kill you.",aliases=["die","assassinate","attack"])
    async def kill(self,ctx,members: commands.Greedy[discord.Member]):
        killQuotes = ["with a rusty spoon","by dropping a piano on them","by beating them with a dildo","by reciting the Bee Movie"
        ,"by doing nothing","by writing their name in the death note.","by throwing their boomerange machete","with the BFG",
        "throwing them into a WoW raid that they were 5 levels too low for.","sheer luck","by releasing the bees"]
        userAlive = True
        for m in members:
            if m == ctx.author:
                await ctx.send('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.LDjJWQejK3vRkuOjvudnLAHaGg%26pid%3DApi&f=1')
            elif m.name == "Wrax the Discord Bot":
                await ctx.send('https://www.youtube.com/watch?v=oJQHH4oPmIA')
            elif randint(0,100) >= 51 and userAlive == True:
                await ctx.send("{} kills {} {}".format(ctx.author.mention,m.mention,choice(killQuotes)))
            elif userAlive == True:
                await ctx.send("{} kills {} {}".format(m.mention,ctx.author.mention,choice(killQuotes)))
                userAlive = False
            else:
                await ctx.send("{} lives.".format(m.mention))



def setup(client):
    client.add_cog(Fun(client))
    
