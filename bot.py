from pyrogram import Client ,filters
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)
@app.on_message(filters.command("start"))
async def start(client, message):
    await app.send_message(message.chat.id, "Bot started")
@app.on_message(filters.command("id"))
async def start(client, message):
    await app.send_message(message.chat.id, f"{message.chat.id}")


app.run()