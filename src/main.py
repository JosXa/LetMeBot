import os
import urllib
from typing import Iterable, Optional
from urllib.parse import urlencode

from aiogram import Bot, Dispatcher, executor
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from aiogram.utils.markdown import quote_html
from loguru import logger

API_TOKEN = os.environ["TOKEN"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def generate_responses(query: str) -> Iterable[InlineQueryResultArticle]:
    encoded_query = urllib.parse.quote(query)
    sites = [
        {
            "ident": "google",
            "url": f"https://google.com/search?q={encoded_query}",
            "name": "🔎 Google",
            "thumb_url": "https://www.google.de/images/hpp/ic_wahlberg_product_core_48.png8.png",
        },
        {
            "ident": "ddg",
            "url": f"https://duckduckgo.com/?q={encoded_query}",
            "name": "🦆 DuckDuckGo",
            "thumb_url": "https://duckduckgo.com/assets/icons/meta/DDG-iOS-icon_152x152.png",
        },
        {
            "ident": "bing-images",
            "url": f"https://www.bing.com/images/search?q={encoded_query}",
            "name": "🖼️ Bing Images",
            "thumb_url": "https://www.gizmochina.com/wp-content/uploads/2020/10/Microsoft-Bing-Logo-2020.jpg",
        },
        {
            "ident": "startpage",
            "url": f"https://www.startpage.com/do/dsearch?query={encoded_query}",
            "name": "🔎 Startpage",
            "thumb_url": "https://www.startpage.com/graphics/favicon/sp-apple-touch-icon-152x152.png",
        },
        {
            "ident": "youtube",
            "url": f"https://www.youtube.com/results?search_query={encoded_query}",
            "name": "📺 YouTube",
            "thumb_url": "https://s.ytimg.com/yts/img/favicon_144-vflWmzoXw.png",
        },
        {
            "ident": "ecosia",
            "url": f"https://ecosia.org/search?q={encoded_query}",
            "name": "🌳 Ecosia",
            "thumb_url": "https://cdn.ecosia.org/assets/images/png/apple-touch-icon.png",
        },
        {
            "ident": "wiki",
            "url": f"https://en.wikipedia.org/wiki/Special:Search/{encoded_query}",
            "name": "📚 Wikipedia",
            "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png",
        },
        {
            "ident": "Wikihow",
            "url": f"https://en.wikihow.com/wikiHowTo?search={encoded_query}",
            "name": "📖 Wikihow",
            "thumb_url": "https://www.wikihow.com/images/7/71/Wh-logo.jpg",
        },
        {
            "ident": "bing",
            "url": f"https://bing.com/search?q={encoded_query}",
            "name": "💩 Bing",
            "thumb_url": "https://logok.org/wp-content/uploads/2014/09/Bing-logo-2013-880x660.png",
        },
        {
            "ident": "ud",
            "url": f"https://www.urbandictionary.com/define.php?term={encoded_query}",
            "name": "📖 Urban Dictionary",
            "thumb_url": "https://a2.mzstatic.com/us/r30/Purple/v4/dd/ef/75/ddef75c7-d26c-ce82-4e3c-9b07ff0871a5/mzl.yvlduoxl.png",
        },
        {
            "ident": "lmgtfy",
            "url": f"https://lmgtfy.com/?q={encoded_query}",
            "name": "🔎  Let Me Google That For You",
            "thumb_url": "https://www.lmgtfy.com/assets/sticker-b222a421fb6cf257985abfab188be7d6746866850efe2a800a3e57052e1a2411.png",
        },
        {
            "ident": "amazon",
            "url": f"https://www.amazon.de/s?field-keywords={encoded_query}",
            "name": "🛒 Amazon",
            "thumb_url": "https://www.turnerduckworth.com/media/filer_public/86/18/86187bcc-752a-46f4-94d8-0ce54b98cd46/td-amazon-smile-logo-01-large.jpg",
        },
        {
            "ident": "telethondocs",
            "url": f"https://lonamiwebs.github.io/Telethon/?q={encoded_query}",
            "name": "📖 Telethon Docs",
        },
    ]

    logger.info(f"Searching for: {query}")
    for site in sites:
        yield InlineQueryResultArticle(
            id=site["ident"],
            title=site["name"],
            description=f"Search for {query}",
            input_message_content=InputTextMessageContent(
                f'<b>{site["name"]}</b>:\n' f'🔎 <a href="{quote_html(site["url"])}">{query}</a>',
                parse_mode="html",
                disable_web_page_preview=True,
            ),
        )


@dp.message_handler(commands=["start", "help"])
async def send_help(message: Message):
    _, args = message.get_full_command()
    if args:
        preset_text = args
    else:
        preset_text = "should you feed squirrels?"

    text = (
        "Hello, i am an inline bot to generate web searches. "
        "Try typing `@letmebot` followed by your search query in any chat "
        "or tap the button below."
    )
    reply_markup = [[InlineKeyboardButton("Try it out", switch_inline_query=preset_text)]]
    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=reply_markup),
        parse_mode="markdown",
        reply=False,
    )


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    query: Optional[str] = inline_query.query

    if not query.strip():
        await bot.answer_inline_query(
            inline_query.id,
            switch_pm_text="Please enter a search term.",
            switch_pm_parameter="help",
            results=[],
            cache_time=1,
        )

    await bot.answer_inline_query(
        inline_query.id, results=list(generate_responses(query)), cache_time=1
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
