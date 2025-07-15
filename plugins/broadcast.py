from pyrogram import Client, filters
from database import users_collection
from info import ADMINS

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        users = users_collection.find()
        sent = 0
        failed = 0
        async for user in client.iter_users(users):
            try:
                await client.send_message(user["user_id"], f"📚 eBookFilterBot Update:\n{text}")
                sent += 1
            except:
                failed += 1
        await message.reply_text(f"Broadcast sent to {sent} users, failed for {failed} users.")
    except:
        await message.reply_text("Usage: /broadcast <message>")

@Client.on_message(filters.private & ~filters.user(ADMINS))
async def save_user(client, message):
    user_id = message.from_user.id
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({
            "user_id": user_id,
            "username": message.from_user.username or "Unknown"
        })
    await message.continue_propagation()
