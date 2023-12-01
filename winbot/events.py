from winbot.handler import commands,welcome,messages
from pyrogram.enums import ChatType
from winbot.config import sudo
import re

async def onMessage(client,message):
    for i in messages:
        if not i.get("group") or message.chat.type != ChatType.PRIVATE:
            await i["callback"](client,message)
    if(message.text):
        userID = str(message.from_user.id)
        text = message.text or ""
        pattern = r'^/(\w+)(?: (.+))?$'
        match = re.match(pattern, text, re.DOTALL)
        if(match):
            name = match.group(1)
            extra = match.group(2) or ""
            if(name in commands and (not commands[f"{name}"].get("group") or message.chat.type != ChatType.PRIVATE) and (not commands[f"{name}"].get("sudo") or userID in sudo)):
                command = commands[f"{name}"] 
                await command["callback"](client,message,extra)
    elif(message.new_chat_members):
        for i in welcome:
            await i['callback'](client,message)