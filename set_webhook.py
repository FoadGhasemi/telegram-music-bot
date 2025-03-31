import requests

BOT_TOKEN = "7789974186:AAFOmZQx8upOgP-JgoHOTn8Cj2eH0E7fhxk"
WEBHOOK_URL = "https://telegram-music-bot-664h.onrender.com/webhook"

response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")

print(response.json())  # Check the response
#python set_webhook.py
