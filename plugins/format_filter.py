from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result

@Client.on_message(filters.command("filter_pdf"))
async def filter_pdf(client, message):
    results = ebooks_collection.find({"format": "PDF"}).limit(5)
    for result in results:
        await message.reply_text(format_result(result))

@Client.on_message(filters.command("filter_epub"))
async def filter_epub(client, message):
    results = ebooks_collection.find({"format": "EPUB"}).limit(5)
    for result in results:
        await message.reply_text(format_result(result))
