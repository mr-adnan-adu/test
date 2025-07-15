from pyrogram import Client, filters
from info import ADMINS, INDEX_CHANNELS
from database import ebooks_collection

@Client.on_message(filters.command("index") & filters.user(ADMINS))
async def index(client, message):
    count = 0
    for channel_id in INDEX_CHANNELS:
        async for msg in client.get_chat_history(channel_id):
            if msg.document and msg.document.mime_type in ["application/pdf", "application/epub+zip", "application/x-mobipocket-ebook"]:
                ebooks_collection.insert_one({
                    "title": msg.caption or msg.document.file_name,
                    "author": "Unknown",
                    "genre": "Unknown",
                    "format": msg.document.mime_type.split("/")[-1].upper(),
                    "language": "Unknown",
                    "file_link": f"https://t.me/c/{channel_id}/{msg.id}",
                    "file_id": msg.document.file_id,
                    "size": f"{msg.document.file_size / 1024 / 1024:.2f}MB"
                })
                count += 1
    await message.reply_text(f"Indexed {count} eBooks.")
