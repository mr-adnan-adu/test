from pyrogram import Client, filters

@Client.on_message(filters.command("echo"))
async def echo(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        await message.reply_text(f"eBook bot echoes: {text}")
    except:
        await message.reply_text("Usage: /echo <text>")
