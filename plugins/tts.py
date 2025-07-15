from pyrogram import Client, filters
from gtts import gTTS
import os

@Client.on_message(filters.command("tts"))
async def tts(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        tts = gTTS(text, lang="en")
        tts.save("data/output.mp3")
        await message.reply_audio("data/output.mp3", caption="TTS by eBook bot")
        os.remove("data/output.mp3")
    except:
        await message.reply_text("Usage: /tts <text>")
