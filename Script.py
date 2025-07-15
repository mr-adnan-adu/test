from pyrogram import Client
from info import API_ID, API_HASH, API_TOKEN, INDEX_CHANNELS
from database import ebooks_collection

app = Client("indexer", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

async def main():
    count = 0
    async with app:
        for channel_id in INDEX_CHANNELS:
            async for msg in app.get_chat_history(channel_id):
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
    print(f"Indexed {count} eBooks.")

app.run(main())
