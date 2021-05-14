import discord,sqlite3
from discord.ext import commands
from discord import Embed

client = commands.Bot(command_prefix='!')

class Database():
    def __init__(self):
        self.database_name = "wrax_database.db"

    async def openDataBase(self):
        db = sqlite3.connect(self.database_name)
        cursor = db.cursor()
        return db,cursor
    
    async def closeDataBase(self,db):
        db.close()
    
    async def getStatusData(self,id):
        db,cursor = await self.openDataBase()
        cursor.execute('''select * from users where user_id = ?''',(id,))
        level,xp,favorite_colors,strength,constitution,dexterity,intelligence,wisdom,charisma,bio = [x for x in cursor.fetchone()[1:]]
        db.close()
        return level,xp,favorite_colors,strength,constitution,dexterity,intelligence,wisdom,charisma,bio

class Status(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.database = Database()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Status Cog is ready!")
    
    async def nextLevelUp(self,level):
        return 50 * (15 * (level+1)) * (level)
    
    async def canLevelUp(self,level,xp):
        max_xp = await self.nextLevelUp(level)
        return xp >= max_xp
    
    async def formatAttributes(self,attributes):
        return "Strength: {}\nConstitution: {}\nDexterity: {}\nIntelligence: {}\nWisdom: {}\nCharisma: {}".format(*attributes)
    
    async def formatXP(self,xp,level):
        return "Level: {}\nXP: {:,}/{:,}".format(level,xp,await self.nextLevelUp(level))
    
    async def formatFavoriteColors(self,favorite_color):
        if favorite_color is None:
            return "None"
        res = ""
        for i in range(len(favorite_color)):
            res += "[{}]: {}\n".format(i,favorite_color[i])
        return res        
    
    @client.command(help="Shows you your current status.",aliases=["me"])
    async def status(self,ctx):
        id = ctx.author.id
        level,xp,favorite_colors,strength,constitution,dexterity,intelligence,wisdom,charisma,bio = await Database().getStatusData(id)
        emb = Embed(title=ctx.author.name,description="AKA {}".format(ctx.author.nick),color=ctx.author.top_role.color)
        emb.add_field(name="Level",value=await self.formatXP(xp,level),inline=False)
        emb.add_field(name="Attributes",value=await self.formatAttributes([strength,constitution,dexterity,intelligence,wisdom,charisma]),inline=False)
        emb.add_field(name="Favorite Colors",value=await self.formatFavoriteColors(favorite_colors.split(",") if favorite_colors is not None else None),inline=False)
        emb.add_field(name="Current Roles",value=",".join([role.name for role in ctx.author.roles]),inline=False)
        emb.add_field(name="Bio",value=bio,inline=False)
        emb.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @client.command(help="Edit your bio on your status.",alias=["write_bio","edit_bio"])
    async def bio(self,ctx,*,bio):
        if len(bio) <= 1024:
            db,cursor = await self.database.openDataBase()
            cursor.execute('''update users set bio = ? where user_id = ?''',(bio,ctx.author.id,))
            await ctx.send("Your bio has been saved!")
            db.commit()
            db.close()
        else:
            await ctx.send("Your bio is too big.")
    
    @commands.Cog.listener()
    async def on_message(self,message):
        await self.client.process_commands(message)
        if message.author.bot is False: 
            author = message.author
            id = author.id
            content = message.content
            xp = int(len(content) * 1.05)
            db,cursor = await self.database.openDataBase()
            cursor.execute('''select xp,level from users where user_id = ?''',(id,))
            print("{} has gained {} xp.".format(message.author.name,xp))
            old_xp,level = [x for x in cursor.fetchone()]
            xp = old_xp + xp
            if await self.canLevelUp(level,xp) is True:
                level += 1
                await message.send("{} has gained a level!".format(message.author.mention))
            cursor.execute('''update users set xp = ?, level = ? where user_id = ?''',(xp,level,id,))
            db.commit()
            db.close()
    
def setup(client):
    client.add_cog(Status(client))