from discord import Embed
from random import choice
from discord.ext import commands
class Help(commands.MinimalHelpCommand):
        
    async def send_pages(self):
        imageList = ["https://i.gifer.com/84U8.gif","https://i.redd.it/9ss8gwpp92851.jpg","https://64.media.tumblr.com/fcb1173a630b9422ea63558524bcdc69/tumblr_mgi2akAMl01r7c13zo1_500.gif",
            "https://i.gifer.com/Nmkp.gif","https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/27a87412-a3b6-4528-9415-eb6e58e5969f/d90l8ks-ac2fdfcc-e620-4bd9-b189-f4eeb39dc7da.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMjdhODc0MTItYTNiNi00NTI4LTk0MTUtZWI2ZTU4ZTU5NjlmXC9kOTBsOGtzLWFjMmZkZmNjLWU2MjAtNGJkOS1iMTg5LWY0ZWViMzlkYzdkYS5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.RCkIb62ohDP5MVswM0C0YWdNsHtjDYh96dRYg685Wzg",
            "https://i.kym-cdn.com/photos/images/original/001/331/586/8c6.gif"]
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

