import asyncio
import discord
from discord.ext import commands
from random import choice, randint, random

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Cog is ready!")
    
    @commands.command(help="Reverses your message.",aliases=["backwards","reverseMessage","reverse_message"])
    async def reverse(self,ctx,*,content):
        await ctx.send(content[::-1])
    
    @commands.command(help="Poke and annoy another member on your server.  This is chosen at random.")
    async def poke(self,ctx):
        target = choice([member for member in await ctx.guild.fetch_members().flatten() if member.bot is False])
        if target.name == ctx.author.name:
            await ctx.send("You've poked yourself")
        else:
            await ctx.send("{} has been poked by {}!".format(target.mention,ctx.author.name))  
    
    @commands.command(help="Kill a member on the server; however, they might kill you.",aliases=["die","assassinate","attack"])
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
    
    @commands.command(help="Play a guessing game with the bot to figure out what number it has.  (After you have used the command, you do need to use prefixes)",alias=['guessnum','guess'])
    async def guessNumber(self,ctx):
        author = ctx.author
        randomNumber,guessedNumber = randint(1,100), -1 #guessed_number is -1 to prevent while loop from being true at start.
        await ctx.send("{0.message.author.mention} I am thinking of a number between 1 and 100...\nEnter the number you think I am guessing.".format(ctx))
        try:
            while guessedNumber != randomNumber:
                def check(message):
                    return message.author == author
                guessedNumber = int( (await self.client.wait_for('message',check=check,timeout=60.0)).content)
                if guessedNumber == randomNumber:
                    await ctx.send("Congrats! **{}** is the number I was thinking of!".format(randomNumber))
                else:
                    if guessedNumber <= 0 or guessedNumber >= 101:
                        await ctx.send("Hey, I said between 1 and 100!")
                    elif guessedNumber > randomNumber:
                        await ctx.send("Nope.  That number is too big.")
                    else:
                        await ctx.send("Nope.  That number is too small.")
        except asyncio.TimeoutError:
            await ctx.send("Huh... you timed out.  The actual number was **{}**".format(randomNumber))

def setup(client):
    client.add_cog(Fun(client))