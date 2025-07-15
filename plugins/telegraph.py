from pyrogram import Client, filters
from telegraph import Telegraph

@Client.on_message(filters.command("telegraph"))
async def telegraph(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        telegraph = Telegraph()
        page = telegraph.create_page("eBook Bot", content=text)
        await message.reply_text(f"Telegraph link for eBook bot: {page['url']}")
    except:
        await message.reply_text("Usage: /telegraph <text>")
