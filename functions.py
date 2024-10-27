import asyncio
import logging
import sys
import os
import aiohttp
import aiogram
import re
import time
import requests


from os import getenv
from aiogram import types
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, Update
from config import *
from button import *
from states import *
from sqlite import *
from check_baza import check
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import sqlite3
from random import randint
from order_info import OrderInfo
from aiogram.filters import BaseFilter, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, ChatMember, ChatMemberLeft

dp = Dispatcher()

def phone_check(value):
    ok = "^[+]998([0-9][012345789]|[0-9][125679]|7[01234569])[0-9]{7}$"
    ok1 = "^998([0-9][012345789]|[0-9][125679]|7[01234569])[0-9]{7}$"

    if re.match(ok, value) or re.match(ok1, value):
        return True
    

async def getAdmin(channel_id):
    try:
        admins = await bot.get_chat_administrators(channel_id)
        for admin in admins:
            if admin.user.id == (await bot.get_me()).id:
                return True
        return False
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False
    
    
async def CheckChannel(channel_id):
    try:
        chat = await bot.get_chat(channel_id)
        return chat
    except Exception as e:
        print(f"Error: {e}")
        return False

def uniqid(prefix='', more_entropy=False):
    m_time = time.time()
    base = '%8x%05x' % (int(m_time), int((m_time - int(m_time)) * 10000000))

    if more_entropy:
        import random
        base += '%.8f' % random.random()

    return prefix + base

def currency_calculator(ga: str, amount: float):
    try:
        url = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        for i in url:
            if ga == i['Ccy']:
                return amount * float(i['Rate'])
    except:
        return False
    