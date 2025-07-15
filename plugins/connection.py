from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.command("connect") & filters.user(ADMINS))
async def connect(client, message):
    if message.chat.type != "private":
        await message.reply_text("Connected to this group for eBook filtering.")
    else:
        await message.reply_text("This command is for groups only.")

@Client.on_message(filters.command("disconnect") & filters.user(ADMINS))
async def disconnect(client, message):
    if message.chat.type != "private":
        await message.reply_text("Disconnected from this group.")
    else:
        await message.reply_text("This command is for groups only.")
