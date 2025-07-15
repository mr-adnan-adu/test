from pyrogram import Client, filters

@Client.on_message(filters.command("fstring"))
async def font_string(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        styled_text = "".join([chr(0x1D5A0 + ord(c) - 97) if c.islower() else c for c in text])
        await message.reply_text(f"Font string for eBook bot: {styled_text}")
    except:
        await message.reply_text("Usage: /fstring <text>")
