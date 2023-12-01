import os
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
plugins = dict(root="winbot.plugins")
sudo = os.environ.get("SUDO").split(",")
database_url = os.environ.get("DATABASE_URL", "")
database_name = os.environ.get("DATABASE_NAME", "")