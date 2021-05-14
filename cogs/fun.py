import discord
from discord.ext import commands
from random import choice

client = commands.Bot(command_prefix="!")

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
    
def setup(client):
    client.add_cog(Fun(client))
    
