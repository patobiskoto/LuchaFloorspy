from datetime import datetime
from config import config
from discord.ext.commands.bot import Bot
from luchaOpensea import OpenseaQuerries
from discord.ext import commands, tasks
from discord import Embed

luchaFloors = commands.Bot(command_prefix = "!", description = "LuchaFloors")

@luchaFloors.event
async def on_ready():
    print('LuchaFloors ready !')
    updateEmbeddedMessage.start()

@tasks.loop(minutes=2.0)
async def updateEmbeddedMessage():
    print(str(datetime.utcnow()) + ': updateEmbeddedMessage')
    if luchaFloors.is_ready:
        messageToUpdate = await Processors.getBotPinnedMessage()
        await messageToUpdate.edit(embed=await Processors.getEmbeddedFloors())
        if messageToUpdate.content == "--init--":
            await messageToUpdate.edit(content="")

class Processors:
    async def getBotPinnedMessage():
        channel = luchaFloors.get_channel(config["discord_channel_id"])
        pins = await channel.pins()
        for pin in pins:
            if pin.author == luchaFloors.user:
                return pin
        sentMessage = await channel.send(content="--init--")
        await sentMessage.pin()
        return sentMessage

    async def getEmbeddedFloors():
        embed = Embed(title="Lucha Floors", description=config["embedded_description"], colour=0x87CEEB, timestamp=datetime.utcnow())
        i = 0
        while i < 8:
            embed.add_field(name=str(i) + "T", value=await OpenseaQuerries.findAFloor(str(i)) + " :eth:", inline=False)
            i = i + 1
        embed.set_footer(text="luchadores.io", icon_url=config["lucha_icon_url"])
        return embed

luchaFloors.run(config["lucha_floor_token_id"])
