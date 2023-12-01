from pyrogram import Client
from pyrogram.types import Message
from winbot.handler import Module


async def gpp(app:Client,message:Message,match:str):
    if message.reply_to_message and message.reply_to_message.photo:
        try:
            if await app.set_chat_photo(message.chat.id,photo=message.reply_to_message.photo.file_id):
                await message.reply("Photo updated succesfully")
            else:
                await message.reply("Failed to upload message")
        except Exception as e:
            print(e)
            await message.reply("Failed to upload message")
    else:
        return await message.reply("No image found")

Module({
    "name":"gpp",
    "description":"group profile setter",
    "group":True,
    "sudo":True
},gpp)
