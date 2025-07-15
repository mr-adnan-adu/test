from pyrogram import Client, filters
from info import ADMINS, INDEX_CHANNELS
from database import ebooks_collection

@Client.on_message(filters.command("add_channel") & filters.user(ADMINS))
async def add_channel(client, message):
    try:
        channel_id = int(message.text.split(" ", 1)[1])
        if channel_id not in INDEX_CHANNELS:
            INDEX_CHANNELS.append(channel_id)
            await message.reply_text(f"Added channel {channel_id} to eBook indexing.")
        else:
            await message.reply_text("Channel already in index list.")
    except:
        await message.reply_text("Usage: /add_channel <channel_id>")

@Client.on_message(filters.command("remove_channel") & filters.user(ADMINS))
async def remove_channel(client, message):
    try:
        channel_id = int(message.text.split(" ", 1)[1])
        if channel_id in INDEX_CHANNELS:
            INDEX_CHANNELS.remove(channel_id)
            ebooks_collection.delete_many({"file_link": {"$regex": f"https://t.me/c/{channel_id}/"}})
            await message.reply_text(f"Removed channel {channel_id} and its eBooks.")
        else:
            await message.reply_text("Channel not in index list.")
    except:
        await message.reply_text("Usage: /remove_channel <channel_id>")
