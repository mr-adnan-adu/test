from pyrogram import Client, filters
from info import BOT_NAME

@Client.on_message(filters.command("bots"))
async def bots_info(client, message):
    await message.reply_text(
        f"📚 {BOT_NAME}\n"
        "Developed by MN Bots, repurposed for eBooks.\n"
        "Use /about for more details."
    )
