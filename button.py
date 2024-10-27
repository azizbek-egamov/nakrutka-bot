from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Buyurtma berish")],
        [KeyboardButton(text="🛒 Buyurtmalarim"), KeyboardButton(text="💵 Hisobim")],
        [KeyboardButton(text="💰 Pul ishlash"), KeyboardButton(text="💳 Pul kiritish")],
        [KeyboardButton(text="📨 Murojaat")]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="◀️ Orqaga")]
    ],
    resize_keyboard=True
)

home = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏘 Asosiy menyu", callback_data="result")]
    ]
)

channels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="plus"),
            InlineKeyboardButton(text="🏘 Asosiy menyu", callback_data="result")
        ],
    ]
)

# ? --- ADMIN PANEL BUTTONS

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="✉️ Xabar yuborish")],
        [KeyboardButton(text="👤 Foydalanuvchini boshqarish")],
        [KeyboardButton(text="〽️ API kalit"), KeyboardButton(text="🗂 Xizmatlar")],
        [KeyboardButton(text="📢 Majburiy obuna"), KeyboardButton(text="💳 To'lov tizimlari")],
        [KeyboardButton(text="🤖 Bot holati"), KeyboardButton(text="◀️ Orqaga")],
    ],
    resize_keyboard=True
)

make_money = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🗣 Referal", callback_data="ref"), InlineKeyboardButton(text="➕ Guruhga odam qo'shish", callback_data="group")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="result")]
    ]
)

aorqaga = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗄 Admin panel")]
    ],
    resize_keyboard=True
)

# admin_panel = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="📊 Statistika", callback_data="statistika")],
#         [InlineKeyboardButton(text="✉️ Xabar yuborish", callback_data="send_message")],
#         [InlineKeyboardButton(text="📢 Majburiy obuna", callback_data="chatjoin")],
#         [InlineKeyboardButton(text="🤖 Bot holati", callback_data="status")],
#         [InlineKeyboardButton(text="🏘 Asosiy menyu", callback_data="result")]
#     ]
# )

send = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Barcha foydalanuvchilarga", callback_data="all_message")],
        [InlineKeyboardButton(text="Bitta foydalanuvchiga", callback_data="user_message")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="panel")]
    ]
)

chatjoins = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_chatjoin"),
         InlineKeyboardButton(text="➖ Kanal o'chirish", callback_data="del_chatjoin")],
        [InlineKeyboardButton(text="📑 Ro'yxat", callback_data="list_chatjoin")],
        [InlineKeyboardButton(text="🗑 Barcha kanallarni olib tashlash", callback_data="del_allchatjoin")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="panel")]
    ]
)

orqaga = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="panel")]
    ]
)