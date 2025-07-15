from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result

@Client.on_message(filters.command("fiction"))
async def filter_fiction(client, message):
    results = ebooks_collection.find({"genre": "Fiction"}).limit(5)
    for result in results:
        await message.reply_text(format_result(result))

@Client.on_message(filters.command("nonfiction"))
async def filter_nonfiction(client, message):
    results = ebooks_collection.find({"genre": "Non-Fiction"}).limit(5)
    for result in results:
        await message.reply_text(format_result(result))
