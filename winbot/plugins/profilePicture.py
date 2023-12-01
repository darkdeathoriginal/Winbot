from winbot.handler import Module

async def run(app,message,match):
    if message.reply_to_message:
        userId = message.reply_to_message.from_user.id
        state = -1
        async for photo in app.get_chat_photos(userId):
            state = 0
            await app.send_photo(message.chat.id,photo.file_id)
        if state == -1:
            return await message.reply("No image found")
    else:
        return await message.reply("Reply to a user")

Module({
    "name":"pp",
    "description":"profile picture finder",
    "sudo":True
},run)