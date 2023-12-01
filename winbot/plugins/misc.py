from winbot.handler import Module
from pyrogram import Client
from pyrogram.types import Message

async def run(app:Client,message:Message,match:str):
    await app.send_message(message.chat.id, message.chat.id)
Module({
    "name":"id",
    "description":"user id"
},run)