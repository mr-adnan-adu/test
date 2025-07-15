from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("paste"))
async def paste(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        response = requests.post("https://pastebin.com/api/api_post.php", data={"text": text})
        await message.reply_text(f"Pasted for eBook bot: {response.text}")
    except:
        await message.reply_text("Usage: /paste <text>")
