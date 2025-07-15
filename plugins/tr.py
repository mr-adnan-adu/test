from pyrogram import Client, filters
from googletrans import Translator

@Client.on_message(filters.command("tr"))
async def translate(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        translator = Translator()
        translated = translator.translate(text, dest="en")
        await message.reply_text(f"Translated for eBook bot: {translated.text}")
    except:
        await message.reply_text("Usage: /tr <text>")
