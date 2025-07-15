from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.command("eval") & filters.user(ADMINS))
async def eval_code(client, message):
    try:
        code = message.text.split(" ", 1)[1]
        exec(code)  # WARNING: Dangerous, use sandbox in production
        await message.reply_text("Evaluated code for eBook bot.")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
