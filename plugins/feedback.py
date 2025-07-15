from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.command("feedback"))
async def feedback(client, message):
    try:
        feedback = message.text.split(" ", 1)[1]
        for admin in ADMINS:
            await client.send_message(admin, f"Feedback from {message.from_user.id}: {feedback}")
        await message.reply_text("Thank you for your feedback on the eBook bot! Suggestions for new eBooks or features are welcome.")
    except:
        await message.reply_text("Usage: /feedback <message>")
