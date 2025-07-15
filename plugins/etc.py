from pyrogram import Client, filters
from info import BOT_NAME

@Client.on_message(filters.command("about"))
async def about(client, message):
    await message.reply_text(
        f"📚 {BOT_NAME}\n"
        "I’m a bot for finding and sharing legally available eBooks (e.g., public domain).\n"
        "Features: Search by title/author/genre, filter by format, and more.\n"
        "Use /start or /search to explore!"
    )

@Client.on_message(filters.command("info"))
async def info(client, message):
    await message.reply_text(
        f"📚 {BOT_NAME} Info\n"
        "Version: 1.0\n"
        "Source: github.com/<your-username>/eBookFilterBot\n"
        "Legal: Only public domain eBooks are shared."
    )
