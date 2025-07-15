from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.command("promote") & filters.user(ADMINS))
async def promote(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        await message.chat.promote_member(user_id, can_pin_messages=True)
        await message.reply_text(f"Promoted {user_id} for eBook bot group.")
    else:
        await message.reply_text("Reply to a user’s message to promote them.")
