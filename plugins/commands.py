from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result
from info import BOT_NAME

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"📚 Welcome to {BOT_NAME}!\n"
        "I help you find and share eBooks. Use /search <query> or /filter_pdf to get started.\n"
        "Note: Only legally available eBooks (e.g., public domain) are shared."
    )

@Client.on_message(filters.command("search"))
async def search(client, message):
    try:
        query = message.text.split(" ", 1)[1]
        results = ebooks_collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
                {"genre": {"$regex": query, "$options": "i"}}
            ]
        }).limit(10)
        for result in results:
            await message.reply_text(format_result(result))
        if not results:
            await message.reply_text("No eBooks found.")
    except:
        await message.reply_text("Usage: /search <query>")

@Client.on_message(filters.command("search_author"))
async def search_author(client, message):
    try:
        author = message.text.split(" ", 1)[1]
        results = ebooks_collection.find({"author": {"$regex": author, "$options": "i"}}).limit(10)
        for result in results:
            await message.reply_text(format_result(result))
        if not results:
            await message.reply_text("No eBooks found for this author.")
    except:
        await message.reply_text("Usage: /search_author <author>")
