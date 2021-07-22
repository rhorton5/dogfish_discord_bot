from discord import Embed
from random import choice
from discord.ext import commands
from json import load

file = open("config.json","r")
json = load(file)
imageList = json['help_image_list']
file.close()

class Help(commands.MinimalHelpCommand):
        
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emb = Embed(description=page)
            emb.set_image(url=choice(imageList))
            await destination.send(embed=emb)

    async def send_command_help(self,command):
        embed = Embed(title=self.get_command_signature(command),description=" ",color= 0x668B8B)
        embed.add_field(name="Descrpition",value=command.help,inline=False)
        embed.add_field(name="Aliases",value=", ".join(command.aliases) if len(command.aliases) != 0 else "N/A",inline=False)
        destination = self.get_destination()
        await destination.send(embed=embed)
    
    async def send_error_message(self, error):
        embed = Embed(title="Error",description=error,color= 0x668B8B)
        channel = self.get_destination()
        await channel.send(embed=embed)

