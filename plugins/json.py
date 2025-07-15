from pyrogram import Client, filters
import json

@Client.on_message(filters.command("json"))
async def json_data(client, message):
    data = message.to_dict()
    await message.reply_text(f"eBook bot JSON:\n```json\n{json.dumps(data, indent=2)}\n```")
