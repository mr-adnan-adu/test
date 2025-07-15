from pyrogram import Client, filters
from database import ebooks_collection
from info import ADMINS

@Client.on_message(filters.command("delete") & filters.user(ADMINS))
async def delete_ebook(client, message):
    try:
        title = message.text.split(" ", 1)[1]
        result = ebooks_collection.delete_one({"title": {"$regex": title, "$options": "i"}})
        if result.deleted_count:
            await message.reply_text(f"Deleted eBook: {title}")
        else:
            await message.reply_text("eBook not found.")
    except:
        await message.reply_text("Usage: /delete <title>")
