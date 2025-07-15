from pyrogram import Client, filters

@Client.on_message(filters.command("sticker"))
async def sticker(client, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        await message.reply_sticker(message.reply_to_message.sticker.file_id)
        await message.reply_text("Sticker sent by eBook bot.")
    else:
        await message.reply_text("Reply to a sticker.")
