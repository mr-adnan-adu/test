from pyrogram import Client, filters
import random, string

@Client.on_message(filters.command("password"))
async def generate_password(client, message):
    length = 12
    password = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    await message.reply_text(f"Generated password for eBook bot: {password}")
