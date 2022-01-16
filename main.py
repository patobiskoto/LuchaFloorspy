from datetime import datetime

from discord import Embed, Activity, ActivityType
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot

from config import config
from luchaOpensea import OpenseaQuerries

luchaFloors = commands.Bot(command_prefix = "!", description = "LuchaFloors")

@luchaFloors.event
async def on_ready():
    print('LuchaFloors ready !')
    update_task.start()

@tasks.loop(minutes=10.0)
async def update_task():
    await luchaFloors.change_presence(activity=Activity(type=ActivityType.watching, name="Refreshing..."))
    await Processors.update_bot_status()
    await Processors.update_embedded_message()
    await luchaFloors.change_presence(activity=Activity(type=ActivityType.watching, name="Luchadores floors"))

class Processors:

    async def update_bot_status():
        print(str(datetime.utcnow()) + ': update_bot_status')
        stats = await OpenseaQuerries.get_collection_stats("luchadores-io")
        for guild in luchaFloors.guilds:
            await guild.me.edit(nick=str(config["bot_name_prefix"]) + str(stats["stats"]["floor_price"]) + str(config["money_visual"]))
        
    async def update_embedded_message():
        print(str(datetime.utcnow()) + ': update_embedded_message')
        if luchaFloors.is_ready:
            messageToUpdate = await Processors._get_bot_pinned_message()
            await messageToUpdate.edit(embed=await Processors._get_embedded_floors())
            if messageToUpdate.content == "--init--":
                await messageToUpdate.edit(content="")

    async def _get_bot_pinned_message():
        channel = luchaFloors.get_channel(int(config["discord_channel_id"]))
        pins = await channel.pins()
        for pin in pins:
            if pin.author == luchaFloors.user:
                return pin
        sentMessage = await channel.send(content="--init--")
        await sentMessage.pin()
        return sentMessage

    async def _get_embedded_floors():
        embed = Embed(title="Lucha Floors", description=config["embedded_description"], colour=0x87CEEB, timestamp=datetime.utcnow())
        i = 0
        while i < 8:
            embed.add_field(name=str(i) + "T", value=str(await OpenseaQuerries.find_a_floor(str(i))) + str(config["money_visual"]), inline=False)
            i = i + 1
        embed.set_footer(text="luchadores.io", icon_url=config["lucha_icon_url"])
        return embed

luchaFloors.run(config["lucha_floor_token_id"])
