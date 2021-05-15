import discord,traceback
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure
client = commands.Bot(command_prefix='!')
class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    def hasRole(ctx):
        return "In Horny Jail" in [role.name for role in ctx.guild.roles]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog is ready!")
    
    @client.command(help="Send somebody to the horny jail",aliases=["horny","hornyJail","hornyjail"])
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
    
    @client.command(help="Changes your top role name",aliases=["changerolename",'rolename'])
    async def change_role_name(self,ctx,*,roleName):
        try:
            top_role = ctx.author.top_role
            old_name = top_role.name
            await top_role.edit(name=roleName)
            await ctx.send("Your role name was changed to {}.\nIt was {}.".format(roleName,old_name))
        except Exception:
            await ctx.send("Role name produced an error...")
            traceback.print_exc()      

def setup(client):
    client.add_cog(Admin(client))