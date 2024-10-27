from aiogram import Bot, Dispatcher, types
import aiohttp
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from bs4 import BeautifulSoup as X
import requests

# tr = Translator()

TOKEN = "7002675047:AAHNlhUyx0GkcCDpCOF92-2tDMb-Ow9xmbU"

channel = ["walpapersUz", "visualcoders"]
admin = "5668945618"
referal = 1000
foiz = 30
api_currency = 'RUB'
group_id = "-1001531445941"
group_url = 'https://t.me/visualcoders_chat'
group_narx = 10

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def botuser():
    bot_info = await bot.get_me()
    return bot_info.username
