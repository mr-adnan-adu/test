from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from database import ebooks_collection
from utils import format_result

@Client.on_inline_query()
async def inline_search(client, query):
    if not query.query:
        return
    results = ebooks_collection.find({
        "$or": [
            {"title": {"$regex": query.query, "$options": "i"}},
            {"author": {"$regex": query.query, "$options": "i"}},
            {"genre": {"$regex": query.query, "$options": "i"}}
        ]
    }).limit(10)
    inline_results = [
        InlineQueryResultArticle(
            title=result["title"],
            input_message_content=InputTextMessageContent(format_result(result)),
            description=f"By {result['author']} ({result['format']})"
        ) for result in results
    ]
    await query.answer(inline_results)
