import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("lookup"))
async def lookup(client, message):
    try:
        title = message.text.split(" ", 1)[1]
        response = requests.get(f"https://openlibrary.org/search.json?title={title}")
        data = response.json()
        if data["docs"]:
            book = data["docs"][0]
            await message.reply_text(
                f"**Book**: {book['title']}\n"
                f"**Author**: {book.get('author_name', ['Unknown'])[0]}\n"
                f"**Subjects**: {', '.join(book.get('subject', ['Unknown']))}"
            )
        else:
            await message.reply_text("No eBook found.")
    except:
        await message.reply_text("Usage: /lookup <title>")
