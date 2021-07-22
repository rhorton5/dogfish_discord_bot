import discord,traceback,typing
from random import randint
from discord.ext import commands
from cogs.status import Database
from re import sub

class Color(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.database = Database()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Color Cog is ready!")
    
    def getRGB(self,argument):
        return [int(x) for x in argument.split(",")]
    
    async def pickRandomRGBValues(self):
        return "{0[0]},{0[1]},{0[2]}".format([randint(0,255) for x in range(3)])
    
    @commands.command(help="Changes your top role color to a new one. If no color is specified, a random one is chosen for you.",aliases=["edit_color","color","rolecolor","changecolor"])
    async def change_color(self,ctx,*,color: typing.Optional[str] = "RANDOM"):
        try:
            if color == "RANDOM":
                color = await self.pickRandomRGBValues()
            r,g,b = self.getRGB(color)
            top_role = ctx.author.top_role
            oR,oG,oB = ctx.author.color.to_rgb()
            await top_role.edit(color=discord.Color.from_rgb(r,g,b))
            await ctx.send("Your color has been changed to ***{},{},{}***\nIt was ***{},{},{}***".format(r,g,b,oR,oG,oB))
        except Exception:
            await ctx.send("Your color has generated an error.")
            traceback.print_exc()
        finally:
            color = None
    
    async def save_favorite_color(self,user_id,color,cursor):
        cursor.execute('''select favorite_colors from users where user_id = ?''',(user_id,))
        temp = cursor.fetchone()[0]
        cur_colors = temp.split(",") if temp is not None else []
        if color in cur_colors:
            return False
        else:
            cur_colors.append(color)
            cursor.execute('''update users set favorite_colors = ? where user_id = ?''',(",".join(cur_colors),user_id,))
            return True
    
    async def delete_favorite_color(self,user_id,index,cursor):
        cursor.execute('''select favorite_colors from users where user_id = ?''',(user_id,))
        temp = cursor.fetchone()[0]
        cur_colors = temp.split(",") if temp is not None else []
        if index < len(cur_colors):
            cur_colors.remove(cur_colors[index])
            cursor.execute('''update users set favorite_colors = ? where user_id = ?''',(",".join(cur_colors),user_id,))
            return True
        return False
    
    async def use_favorite_color(self,user,user_id,index,cursor):
        cursor.execute('''select favorite_colors from users where user_id = ?''',(user_id,))
        temp = cursor.fetchone()[0]
        cur_colors = temp.split(",") if temp is not None else []
        if index < len(cur_colors):
            r,g,b = [int(sub("[\D]","",x)) for x in cur_colors[index].split(" ")]
            await user.top_role.edit(color=discord.Color.from_rgb(r,g,b))
            return True
        return False
    
    @commands.command(help="Allows you to use the favorite colors you've saved.\n\n**Subcommands** \nsave <r,g,b> -> Saves color to your list\ndelete <index> -> Deletes a color from your list\nuse <index> -> Change role color to a color in the list.",
                    aliases=["fav_color","favcolor","favoritecolor","favColor","favoriteColor"])
    async def favorite_color(self,ctx,type: str, *, color):
        #Add a way to view colors from favorite_color...
        db, cursor = await self.database.openDataBase()
        if type.lower() == "save":
            color = "[" + color.replace(","," ") + "]"
            if await self.save_favorite_color(ctx.author.id,color,cursor) is True:
                await ctx.send("{} was saved.  You may view it with the status command.".format(color))
            else:
                await ctx.send("{} is already in your list.".format(color))
        
        elif type.lower() == "delete":
            if await self.delete_favorite_color(ctx.author.id,int(color),cursor) is True:
                await ctx.send("{} was deleted.".format(color))
            else:
                await ctx.send("{} is not in your list.".format(color))
        elif type.lower() == "use":
            if await self.use_favorite_color(ctx.author,ctx.author.id,int(color),cursor) is True:
                await ctx.send("Your color has been set.")
            else:
                await ctx.send("Invalid index.")       
        db.commit()
        db.close()


def setup(client):
    client.add_cog(Color(client))