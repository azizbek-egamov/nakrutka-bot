from aiogram import BaseMiddleware
from aiogram.types import InlineKeyboardButton, Update, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import bot
from functions import *
from sqlite import *
from states import phone_add
DEFAULT_RATE_LIMIT = .1


class check(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix

    async def __call__(self, handler, event: Update, data):
        if event.message:
            user_id = event.message.chat.id
            user = event.message.chat
        elif event.callback_query:
            user_id = event.callback_query.message.chat.id
            user = event.callback_query.message.chat
            

        r = table_info("users", "uid", user_id)
        if r == False:
            add_information(user_id, user.full_name, user.username, 0, 0, 0, 0, 'false')
            return await handler(event, data)
        else:
            return await handler(event, data)
            
