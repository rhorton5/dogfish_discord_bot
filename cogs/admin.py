import discord,traceback
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, ChannelNotFound, ChannelNotReadable, MessageNotFound

class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    def hasRole(ctx):
        return "In Horny Jail" in [role.name for role in ctx.guild.roles]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog is ready!")
    
    @commands.command(help="Send somebody to the horny jail",aliases=["horny","hornyJail","hornyjail"])
    @commands.check(hasRole)
    async def horny_jail(self,ctx,members: commands.Greedy[discord.Member]):
        msg = ""
        for role in await ctx.guild.fetch_roles():
            if role.name == "In Horny Jail":
                hornyJailRole = role
        for member in members:
            if hornyJailRole in member.roles:
                await member.remove_roles(hornyJailRole)
                msg += "{} is being let out of the horny jail.\n".format(member.name)
            else:
                await member.add_roles(hornyJailRole)
                msg += "{}!  You're going to horny jail!\n".format(member.name)
        await ctx.send(msg)
    
    @horny_jail.error
    async def on_error(self,ctx,error):
        if isinstance(error,CheckFailure):
            await ctx.send("You do not have the horny jail role.  Please add that before running the program again.")
        else:
            await ctx.send("Some other error has occured.")
    
    @commands.command(help="Changes your top role name",aliases=["changerolename",'rolename'])
    async def change_role_name(self,ctx,*,roleName):
        try:
            top_role = ctx.author.top_role
            old_name = top_role.name
            await top_role.edit(name=roleName)
            await ctx.send("Your role name was changed to {}.\nIt was {}.".format(roleName,old_name))
        except Exception:
            await ctx.send("Role name produced an error...")
            traceback.print_exc()

    @commands.command(help="Moves a message to a new channel.  The channel will be embed since the purpose is to 'pin' items with actually doing so.  ***IMPORTANT***: You must use the command on the channel where the message was posted.",aliases=['valhalla'])
    async def move_message(self,ctx,message: discord.Message,destChannel: discord.TextChannel):
        emb = discord.Embed(title=f"{message.author.nick}'s post has made it to Valhalla!",description="",color=message.author.top_role.color)
        if len(message.content) != 0: #Messages can have content despite having no words in them.
            print(message.content)
            emb.add_field(name="\u200b",value=message.content,inline=False) #\u200b is whitespace, this gets rid of the title without having to write one.
        emb.add_field(name="\u200b",value=f"Original Link: {message.jump_url}",inline=False)
        print(message.attachments)
        if message.attachments:
            emb.set_image(url=message.attachments[0].url)
        emb.set_author(name=message.author.name,icon_url=message.author.avatar_url)
        await destChannel.send(embed=emb)
        await ctx.message.delete()
    
    @move_message.error
    async def on_error(self,ctx,error):
        if isinstance(error,ChannelNotFound):
            await ctx.send("The channel was not found.")
        elif isinstance(error,ChannelNotReadable):
            await ctx.send("I cannot send the message to the channel.")
        elif isinstance(error,MessageNotFound):
            await ctx.send("The message was not found.")
        else:
            await ctx.send("Some other error has occured.")


def setup(client):
    client.add_cog(Admin(client))