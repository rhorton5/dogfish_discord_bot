from discord import guild
from discord.ext import commands
from operator import add
import discord
import sqlite3

class Setting(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.databaseName = "wrax_database.db"
  
    @commands.command(help="Changes prefix for this bot.",alias=['prefix'])
    async def setPrefix(self,ctx,prefix):
        db = sqlite3.connect(self.databaseName)
        cursor = db.cursor()
        cursor.execute('''update Guild set prefix = ? where guild_id = ?''',(prefix,ctx.guild.id,))
        db.commit()
        db.close()
        await ctx.send("Prefix has been set to {}".format(prefix))   
    
    @commands.command(help="Allows you to make a channel muted.  No commands will be responded to said channel.")
    async def mutedChannel(self,ctx,subcommand: str,channels: commands.Greedy[discord.TextChannel]):
        db = sqlite3.connect(self.databaseName)
        cursor = db.cursor()
        guild_id = ctx.guild.id
        cursor.execute('''select muted_channels_ids from Guild where guild_id = ?''',(guild_id,))
        db_fetch = cursor.fetchone()[0]
        muted_channels_ids = [str(channel_id) for channel_id in db_fetch.split(", ")] if db_fetch != None else [] #Contains the list from the database.
        requested_channels = [str(c.id) for c in channels] #Contains the list of requested channels form the command.

        if subcommand == "add":
            muted_channels_ids = list(set(muted_channels_ids + requested_channels))
            print(muted_channels_ids)
            cursor.execute('''update Guild set muted_channels_ids = ? where guild_id = ?''',(", ".join(muted_channels_ids),guild_id,))
            db.commit()
            await ctx.send(f"{','.join([channel.name for channel in channels])} have been added to your muted channel list for {ctx.guild.name}.")

        elif subcommand == "remove":
            muted_channels_ids = [channel for channel in muted_channels_ids if channel not in requested_channels] #remove any channels included in the requested channels list.
            cursor.execute('''update Guild set muted_channels_ids = ? where guild_id = ?''',(", ".join(muted_channels_ids),guild_id,))
            db.commit()
            await ctx.send(f"{','.join([channel.name for channel in channels])} have been removed from the muted channel list for {ctx.guild.name}.")
        else:
            await ctx.send(f"**Error**: {subcommand} is not a valid command")
        db.close()
    
def setup(client):
    client.add_cog(Setting(client))

