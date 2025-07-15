from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.command("pin") & filters.user(ADMINS))
async def pin(client, message):
    if message.reply_to_message:
        await message.reply_to_message.pin()
        await message.reply_text("Pinned eBook bot message.")
    else:
        await message.reply_text("Reply to a message to pin it.")
