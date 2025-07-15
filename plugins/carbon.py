from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("carbon"))
async def carbon(client, message):
    try:
        code = message.text.split(" ", 1)[1]
        response = requests.post("https://carbon.now.sh", json={"code": code})
        await message.reply_photo(response.url, caption="Code snippet for eBook bot.")
    except:
        await message.reply_text("Usage: /carbon <code>")
