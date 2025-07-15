from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("short"))
async def shorten_url(client, message):
    try:
        url = message.text.split(" ", 1)[1]
        response = requests.get(f"https://is.gd/create.php?format=simple&url={url}")
        await message.reply_text(f"Shortened eBook link: {response.text}")
    except:
        await message.reply_text("Usage: /short <url>")
