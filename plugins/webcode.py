from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result

@Client.on_message(filters.command("weblink"))
async def weblink(client, message):
    try:
        title = message.text.split(" ", 1)[1]
        result = ebooks_collection.find_one({"title": {"$regex": title, "$options": "i"}})
        if result:
            await message.reply_text(f"eBook Web Link: {result['file_link']}")
        else:
            await message.reply_text("eBook not found.")
    except:
        await message.reply_text("Usage: /weblink <title>")
