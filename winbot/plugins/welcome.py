from winbot.handler import onJoin,Module
from pyrogram import Client
from pyrogram.types import Message,User
from winbot.database.welcome import addWelcome,findWelcome

async def join(app:Client,message:Message):
    group = await app.get_chat(message.chat.id)
    groupName = group.title
    groupDescription = group.description
    userName = message.new_chat_members[0].username
    userId = message.new_chat_members[0].id
    found = await findWelcome(message.chat.id)
    if found:
        text = found["text"]
        if "{mention}" in text:
            text = text.replace("{mention}", "@"+userName)
        if "{title}":
            text = text.replace("{title}", groupName)
        if "{desc}":
            text = text.replace("{desc}", groupDescription)
        if "{pp}" in text:
            text = text.replace("{pp}","")
            photos =  []
            async for photo in app.get_chat_photos(userId):
                photos.append(photo)
            if len(photos)>0:
                return await app.send_photo(message.chat.id,photos[-1].file_id,text)
        return await app.send_message(message.chat.id,text)

onJoin({},join)

async def run(app:Client,message:Message,match:str):
    if match == "":
        text = 'use:\n{pp} for adding profile picture\n{mention} for mentioning the member\n{title} for group title\n{desc} for group description\n\nexample:/welcome {pp}Hello {mention}, welcome to {title}\n {desc}'
        return await message.reply(text)
    text = match
    await addWelcome(message.chat.id,text)
    return await message.reply("welcome added")

Module({
    "name":"welcome",
    "description":"Welcome message setter",
    "group":True,
    "sudo":True
},run)