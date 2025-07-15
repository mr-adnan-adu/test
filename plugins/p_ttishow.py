from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result

@Client.on_message(filters.command("show"))
async def show_ebook(client, message):
    try:
        title = message.text.split(" ", 1)[1]
        result = ebooks_collection.find_one({"title": {"$regex": title, "$options": "i"}})
        if result:
            await message.reply_text(format_result(result))
        else:
            await message.reply_text("eBook not found.")
    except:
        await message.reply_text("Usage: /show <title>")
