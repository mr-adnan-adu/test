from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result

@Client.on_message(filters.group & filters.text & ~filters.command)
async def auto_filter(client, message):
    query = message.text
    results = ebooks_collection.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"author": {"$regex": query, "$options": "i"}},
            {"genre": {"$regex": query, "$options": "i"}}
        ]
    }).limit(5)
    for result in results:
        await message.reply_text(format_result(result))
