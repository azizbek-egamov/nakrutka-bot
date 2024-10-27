from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from button import *
from sqlite import *
from states import *
from config import admin
from functions import bot
import time
import requests

orders_dp = Router()
router = orders_dp


@router.message(F.text == "🛒 Buyurtmalarim")
async def OrderInfoPage(message: Message):
    uid = message.chat.id
    res = table_info("orders", "uid", uid)
    if res != False:
        btn = InlineKeyboardBuilder()
        for i in res:
            btn.add(
                InlineKeyboardButton(
                    text=f"🆔 {i[2]}", callback_data=f"orderinfo-{i[2]}"
                )
            )
        btn.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="result"))
        btn.adjust(3)

        await message.answer(
            text="<b>✔️ Kerakli buyurtmani tanlang.</b>", reply_markup=btn.as_markup()
        )
    else:
        await message.answer(
            text="<b>💁🏻‍♂️ Sizda hali buyurtmalar yo'q</b>", reply_markup=menu
        )


@router.callback_query(F.data == "oorders")
async def OrderInfoPagec(callback: CallbackQuery):
    await callback.message.delete()
    uid = callback.message.chat.id
    res = table_info("orders", "uid", uid)
    if res != False:
        btn = InlineKeyboardBuilder()
        for i in res:
            btn.add(
                InlineKeyboardButton(
                    text=f"🆔 {i[2]}", callback_data=f"orderinfo-{i[2]}"
                )
            )
        btn.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="result"))
        btn.adjust(3)

        await callback.message.answer(
            text="<b>✔️ Kerakli buyurtmani tanlang.</b>", reply_markup=btn.as_markup()
        )
    else:
        await callback.message.answer(
            text="<b>💁🏻‍♂️ Sizda hali buyurtmalar yo'q</b>", reply_markup=menu
        )


@router.callback_query(F.data.startswith("orderinfo-"))
async def OrderInfoPage2(callback: CallbackQuery):
    await callback.message.delete()
    order_id = callback.data.split("-")[1]
    uid = callback.message.chat.id
    res = one_table_info("orders", "order_id", order_id)
    if res != False:
        if str(res[1]) == str(uid):
            api_key = one_table_info("api_key", "uid", admin)
            if api_key != False:
                cv = await callback.message.answer("<b>🕔 Iltimos kutib turing.</b>")
                url = requests.get(
                    f"{api_key[3]}/?key={api_key[2]}&action=status&order={order_id}"
                ).json()
                if ("error" in url) == False:
                    if url["status"] == "Canceled":
                        icon = '🚫'
                        status = "Bekor qilingan"
                    elif url["status"] == "Completed":
                        status = "Bajarilgan"
                        icon = '✔️'
                    elif url["status"] == "Partial":
                        icon = '⏏️'
                        status = "Qisman bajarilgan"
                    elif url["status"] == "In progress":
                        icon = '〽️'
                        status = "Jarayonda"
                    elif url["status"] == "Pending":
                        icon = '🔄'
                        status = "Kutilmoqda"
                    await bot.delete_message(uid, cv.message_id)
                    await callback.message.answer(
                        text=f"""<b>ℹ️ Buyurtma haqida ma'lumotlar.</b>
                        
<b>📎 ID raqami:</b> <i>{order_id}</i>
<b>◽️ Xizmat nomi:</b> <i>{res[5]}</i>
<b>◾️ Buyurtma miqdori:</b> <i>{res[7]} ta</i>
<b>💰 Buyurtma narxi:</b> <i>{"{:.2f}".format(float(res[6]))} so'm</i>

<b>{icon} Buyurtma holati:</b> <i>{status}</i>""",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text="◀️ Orqaga", callback_data="oorders"
                                    )
                                ]
                            ]
                        ),
                    )
                else:
                    await callback.message.answer(
                        text="<b>⚠️ Ma'lumotlarni olishda xatolik yuz berdi.</b>",
                        reply_markup=menu,
                    )
            else:
                await callback.message.answer(
                    text="<b>⚠️ Ma'lumotlarni olishda xatolik yuz berdi.</b>",
                    reply_markup=menu,
                )
        else:
            await callback.message.answer(
                text="<b>⚠️ Buyurtma siza tegishli emas.</b>", reply_markup=menu
            )
    else:
        await callback.message.answer(
            text="<b>⚠️ Buyurtma topilmadi.</b>", reply_markup=menu
        )
