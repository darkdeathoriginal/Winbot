from pyrogram import Client ,filters
from pyrogram.types import BotCommand
from pyrogram.handlers import MessageHandler
from winbot.config import api_hash,api_id,bot_token,plugins
from winbot.handler import commands
from winbot.events import onMessage

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins=plugins
)

async def setCommands():
    clist = []
    for i in commands.values():
        clist.append(BotCommand(i["name"],i["description"]))
    await app.set_bot_commands(clist)



app.add_handler(MessageHandler(onMessage))


app.start()
async def main():
    print("Bot started")
    await setCommands()
app.loop.run_until_complete(main())
app.loop.run_forever()