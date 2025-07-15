from pyrogram import Client, filters
from info import ADMINS
import subprocess

@Client.on_message(filters.command("shell") & filters.user(ADMINS))
async def shell(client, message):
    try:
        cmd = message.text.split(" ", 1)[1]
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        await message.reply_text(f"Shell output for eBook bot:\n{result.stdout}")
    except:
        await message.reply_text("Usage: /shell <command>")
