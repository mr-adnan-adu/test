from pyrogram import Client, filters
import time

@Client.on_message(filters.command("ping"))
async def ping(client, message):
    start = time.time()
    msg = await message.reply_text("Pinging...")
    end = time.time()
    await msg.edit_text(f"🏓 Pong! {round((end - start) * 1000)}ms")
