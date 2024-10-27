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

payment_dp = Router()
router = payment_dp


@router.message(F.text == "💳 Pul kiritish")
async def PulKirit(message: Message):
    res = select_info("pay_cards")
    if res != False:
        btn = InlineKeyboardBuilder()
        for i in res:
            btn.add(InlineKeyboardButton(text=str(i[1]), callback_data=f"paym-{i[0]}"))
        btn.adjust(2)
        await message.answer(
            text="<b>💳 Kerakli to'lov tizimini tanlang.</b>",
            reply_markup=btn.as_markup(),
        )
    else:
        await message.answer(
            text="<b>💁🏻‍♂️ To'lov qilish uchun hamyonlar topilmadi.</b>",
            reply_markup=menu,
        )


@router.callback_query(F.data.startswith("paym-"))
async def PulKirit2(callback: CallbackQuery):
    id = callback.data.split("-")[1]
    res = one_table_info("pay_cards", "id", id)
    await callback.message.delete()
    if res != False:
        await callback.message.answer(
            text=f"""<b>{res[1]} hamyoni ma'lumotlari.
            
💳 Hammyon raqami: <code>{res[2]}</code>
ℹ️ Qo'shimcha ma'lumot:</b> <i>{res[3]}</i>

<i>◽️ Bot hozirda avtomatik to'lov xizmatlarini qo'llab quvvatlamaydi, shuning uchun o'zingiz to'lov qilishingiz va chekni botga yuborishingiz so'raladi.</i>""",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="✅ To'lovni amalga oshirdim",
                            callback_data=f"payqildi-{id}",
                        )
                    ],
                    [InlineKeyboardButton(text="❌ Yopish", callback_data="result")],
                ]
            ),
        )
    else:
        await callback.message.answer(
            text="<b>💁🏻‍♂️ To'lov qilish uchun hamyon topilmadi.</b>",
            reply_markup=menu,
        )


@router.callback_query(F.data.startswith("payqildi-"))
async def Payqildi(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split("-")[1]
    await callback.message.delete()
    await callback.message.answer(
        text="<b>◽️ To'lov miqdorini kiriting.</b>",
        reply_markup=back,
    )
    await state.update_data({"id": id})
    await state.set_state(Payments.count)


@router.message(Payments.count)
async def Payqildi2(message: Message, state: FSMContext):
    txt = message.text
    if str(message.text).isdigit():
        if int(txt) >= 5000:
            await message.answer(
                text="<b>📄 To'lovni qilganingiz haqidagi screenshotni yuboring.</b>",
                reply_markup=back,
            )
            await state.update_data({"count": txt})
            await state.set_state(Payments.rasm)
        else:
            await message.answer(
            text="<b>⚠️ Minimal to'lov miqdori 5000 so'm.</b>", reply_markup=back
        )
    else:
        await message.answer(
            text="<b>⚠️ Faqat raqamlardan foydalaning.</b>", reply_markup=back
        )


@router.message(Payments.rasm)
async def Payqildi3(message: Message, state: FSMContext):
    if message.photo:
        data = await state.get_data()
        id = data.get("id")
        count = data.get("count")
        await message.answer(
            text="<b>🕔 So'rov administratorga yuborildi, tez orada so'rovingiz tekshiriladi va balansingizga pullar tushurib beriladi.</b>",
            reply_markup=menu,
        )
        res = one_table_info("pay_cards", "id", id)
        await bot.send_photo(
            chat_id=admin,
            photo=str(message.photo[-1].file_id),
            caption=f"""<b>✔️ Yangi hisob to'ldirish so'rovi kelib tushdi.
            
👤 Foydalanuvchi: {message.chat.full_name}
🆔 ID raqami: <a href='tg://user?id={message.chat.id}'>{message.chat.id}</a>
💰 To'lov miqdori: {count} so'm

ℹ️ Ma'lumotlar to'gri bo'lsa '✅ Tastiqlash' tugmasini bosing</b>""",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="✅ Tastiqlash",
                            callback_data=f"ok-{message.chat.id}-{count}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="❌ Bekor qilish",
                            callback_data=f"no-{message.chat.id}",
                        )
                    ],
                ]
            ),
        )
        await state.clear()
    else:
        await message.answer(
            text="<b>⚠️ Faqat rasm formatdagi ma'lumot qabul qilinadi.</b>",
            reply_markup=back,
        )


@router.callback_query(F.data.startswith("ok-"))
async def Payqildi4(callback: CallbackQuery):
    action = callback.data.split("-")
    id = action[1]
    count = action[2]
    await callback.message.delete()
    await callback.message.answer(
        f"<b>✅ To'lov tastiqlandi va foydalanuvchi balansiga {count} so'm qo'shildi</b>"
    )
    await bot.send_message(
        chat_id=str(id),
        text=f"""<b>✅ To'lovingiz tastiqlandi va balansingizga {count} so'm qo'shildi.</b>""",
    )
    r = one_table_info("users", "uid", id)
    UpdateUsersBalance(id, float(r[4]) + int(count))
    UpdateUsersPayment(id, float(r[6]) + int(count))


@router.callback_query(F.data.startswith("no-"))
async def Payqildi4(callback: CallbackQuery):
    action = callback.data.split("-")
    id = action[1]
    await callback.message.delete()
    await callback.message.answer(f"<b>❌ To'lov tastiqlanmadi</b>")
    await bot.send_message(
        chat_id=str(id), text=f"""<b>❌ To'lovingiz tastiqlanmadi, agar haqiqatdan to'lov qilgan bo'lsangiz administrator bilan aloqaga chiqing</b>""",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🧑🏻‍💻 Administrator", url=f"tg://user?id={admin}")]
            ]
        )
    )


