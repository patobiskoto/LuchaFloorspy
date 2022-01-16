from datetime import datetime

from discord import Embed
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot

from config import config
from luchaOpensea import OpenseaQuerries

luchaFloors = commands.Bot(command_prefix = "!", description = "LuchaFloors")

@luchaFloors.event
async def on_ready():
    print('LuchaFloors ready !')
    updateEmbeddedMessage.start()

@tasks.loop(seconds=10.0)
async def updateEmbeddedMessage():
    print(str(datetime.utcnow()) + ': updateEmbeddedMessage')
    if luchaFloors.is_ready:
        messageToUpdate = await Processors.getBotPinnedMessage()
        await messageToUpdate.edit(embed=await Processors.getEmbeddedFloors())
        if messageToUpdate.content == "--init--":
            await messageToUpdate.edit(content="")

class Processors:
    async def getBotPinnedMessage():
        channel = luchaFloors.get_channel(int(config["discord_channel_id"]))
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
            print("-- request for " + str(i) + "T")
            embed.add_field(name=str(i) + "T", value=str(await OpenseaQuerries.findAFloor(str(i))) + "Ξ", inline=False)
            i = i + 1
        embed.set_footer(text="luchadores.io", icon_url=config["lucha_icon_url"])
        return embed

luchaFloors.run(config["lucha_floor_token_id"])
