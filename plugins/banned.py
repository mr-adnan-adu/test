from pyrogram import Client, filters
from database import bans_collection
from info import ADMINS

@Client.on_message(filters.command("ban") & filters.user(ADMINS))
async def ban_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bans_collection.insert_one({"user_id": user_id})
        await message.reply_text(f"User {user_id} banned from eBookFilterBot.")
    else:
        await message.reply_text("Reply to a user's message to ban them.")

@Client.on_message(filters.command("unban") & filters.user(ADMINS))
async def unban_user(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bans_collection.delete_one({"user_id": user_id})
        await message.reply_text(f"User {user_id} unbanned from eBookFilterBot.")
    else:
        await message.reply_text("Reply to a user's message to unban them.")

@Client.on_message(filters.private & ~filters.user(ADMINS))
async def check_ban(client, message):
    user_id = message.from_user.id
    if bans_collection.find_one({"user_id": user_id}):
        await message.reply_text("You are banned from using eBookFilterBot.")
        return
    await message.continue_propagation()
