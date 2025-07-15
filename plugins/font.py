from pyrogram import Client, filters

@Client.on_message(filters.command("font"))
async def font(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        styled_text = "".join([chr(0x1D670 + ord(c) - 65) if c.isalpha() else c for c in text.upper()])
        await message.reply_text(f"Styled text for eBook bot: {styled_text}")
    except:
        await message.reply_text("Usage: /font <text>")
