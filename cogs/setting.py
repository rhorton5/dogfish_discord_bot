from discord.ext import commands
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
    


def setup(client):
    client.add_cog(Setting(client))

