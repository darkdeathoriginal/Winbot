import time
from pyrogram import Client
from pyrogram.types import Message
from winbot.handler import Module,commands


async def run(app:Client,message:Message,match:str):
    start_time = int(time.time() * 1000)
    await app.send_message(message.chat.id, "❮ ᴛᴇsᴛɪɴɢ ᴘɪɴɢ ❯")
    end_time = int(time.time() * 1000)
    await app.send_message(message.chat.id, f"ʟᴀᴛᴇɴᴄʏ: {end_time - start_time} ᴍs")

Module({
    "name":"ping",
    "description":"ping command"
},run)

async def start(app:Client,message:Message,match:str):
    msg ='Welcome to winbot\nThis is a bot to manage your group\n\nCommands:\n'
    for i in commands:
        msg += f"/{i} : {commands[i]['description']} "
        if commands[i].get('group'):
            msg +='(Group Only), '
        if commands[i].get('sudo'):
            msg +='(Admin Only)'
        msg +='\n'
        print(i)
    await app.send_message(message.chat.id, msg)

Module({
    "name":"start",
    "description":"start command"
},start)


