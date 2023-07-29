import os
from dotenv import load_dotenv
load_dotenv()

# parse environment variables
env = {key: os.getenv(key).split(',') if os.getenv(key) else [] for key in os.environ}


# Variables
tg = env.get('TELEGRAM_TOKEN', [])[0]
key = env.get('STABLEHORDE_KEY', [])[0]
#


base_url = "https://ratings.aihorde.net/api/v1/rating"

headers = {'Apikey': key}



emojis_rating = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
emojis_artifacts = ["😍", "😐", "🤔", "😖", "🤮"]

from .database import JsonDatabase
db = JsonDatabase()
