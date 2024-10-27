from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from button import *
from sqlite import *
from states import *
from config import admin, foiz
from functions import bot, currency_calculator, api_currency
import time
import requests

services_dp = Router()
router = services_dp

data = select_info("category")
page_sizee = 10
sub_page_size = 10


def paginate_data(data, page_size=page_sizee):
    if data != False:
        return [data[i : i + page_size] for i in range(0, len(data), page_size)]
    else:
        return False


pages = paginate_data(data)


def get_keyboard(page: int):
    builder = InlineKeyboardBuilder()

    start_index = page * page_sizee
    for i, item in enumerate(pages[page]):
        builder.add(
            InlineKeyboardButton(
                text=str(start_index + i + 1),
                callback_data=f"category:{item[0]}:0:{page}",
            )
        )
    builder.adjust(5)

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"prev:{page-1}")
        )
    if page < len(pages) - 1:
        navigation_buttons.append(
            InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"next:{page+1}")
        )

    if navigation_buttons:
        builder.row(*navigation_buttons)

    return builder.as_markup()


@router.message(F.text == "📦 Buyurtma berish")
async def send_welcome(message: Message):
    res = select_info("category")
    delete_table("order_temp", 'uid', message.chat.id)
    if res != False:
        await send_page(message.chat.id, 0)
    else:
        await message.answer(
            text="<b>⚠️ Kategoriyalar mavjud emas.</b>", reply_markup=menu
        )


@router.callback_query(F.data.startswith("add_order::"))
async def adds_service(callback: CallbackQuery):
    res = select_info("category")
    await callback.message.delete()

    if res != False:
        id = callback.data.split("::")[1]
        await send_page(callback.message.chat.id, int(id))
    else:
        await callback.message.answer(
            text="<b>⚠️ Kategoriyalar mavjud emas</b>", reply_markup=menu
        )


async def send_page(chat_id: int, page: int):
    if 0 <= page < len(pages):
        start_index = page * page_sizee
        text = "\n".join(
            [f"{start_index + i + 1}: {item[1]}" for i, item in enumerate(pages[page])]
        )
        keyboard = get_keyboard(page)
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>🗄 Kerakli katagoriyani tanlang:\n\n<i>{text}</i></b>",
            reply_markup=keyboard,
        )


@router.callback_query(
    lambda c: c.data
    and (
        c.data.startswith("page:")
        or c.data.startswith("next:")
        or c.data.startswith("prev:")
    )
)
async def process_callback(callback_query: CallbackQuery):
    data = callback_query.data.split(":")
    action = data[0]
    page = int(data[1])

    await callback_query.answer()

    if action == "prev" and page > 0:
        await send_page(callback_query.message.chat.id, page)
    elif action == "next" and page < len(pages):
        await send_page(callback_query.message.chat.id, page)

    await callback_query.message.delete()


def paginate_sub_data(data, page_size=sub_page_size):
    return [data[i : i + page_size] for i in range(0, len(data), page_size)]


def get_sub_keyboard(category_id, sub_page, sub_pages, pg):
    builder = InlineKeyboardBuilder()

    start_index = sub_page * sub_page_size
    for i, item in enumerate(sub_pages[sub_page]):
        builder.add(
            InlineKeyboardButton(
                text=str(start_index + i + 1),
                callback_data=f"service:{category_id}:{sub_page}:{pg}:{item[0]}",
            )
        )

    navigation_buttons = []
    if sub_page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data=f"category:{category_id}:{sub_page-1}:{pg}",
            )
        )
    if sub_page < len(sub_pages) - 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data=f"category:{category_id}:{sub_page+1}:{pg}",
            )
        )

    builder.adjust(5)

    order_back = [
        InlineKeyboardButton(text="◀️ Orqaga", callback_data=f"add_order::{pg}")
    ]
    if navigation_buttons:
        builder.row(*navigation_buttons)

    if order_back:
        builder.row(*order_back)

    return builder.as_markup()


@router.callback_query(F.data.startswith("category:"))
async def CategInfoPahe(callback: CallbackQuery):
    category_id, sub_page, pg = callback.data.split(":")[1:]
    sub_page = int(sub_page)
    pg = int(pg)
    print(category_id)
    res = table_info("services", "category_id", category_id)
    tr = one_table_info("category", "id", category_id)

    if res:
        await callback.answer('◽️ 1 soniya, ma\'lumotlar yuklanmoqda')
        sub_pages = paginate_sub_data(res)
        start_index = sub_page * sub_page_size
        text = "\n".join(
            [
                f"<b>{start_index + i + 1}:</b> <i>{item[2]}</i><b>, Narxi (1000 ta)</b>: <i>{"{:.2f}".format((currency_calculator(api_currency, float(item[4]))) + (currency_calculator(api_currency, float(item[4])) / 100) * foiz)} so'm</i>"
                for i, item in enumerate(sub_pages[sub_page])
            ]
        )
        keyboard = get_sub_keyboard(category_id, sub_page, sub_pages, pg)
        await callback.message.edit_text(
            text=f"<b><i>🗄 Kategoriya: {tr[1]}\n◽️ Kerakli xizmatni tanlang:</i></b>\n\n{text}",
            reply_markup=keyboard,
        )
        await callback.answer()
    else:
        await callback.message.delete()
        await callback.message.answer(
            text="<b>⚠️ Ushbu kategoriya uchun xizmatlar topilmadi.</b>",
            reply_markup=menu,
        )


@router.callback_query(F.data.startswith("service:"))
async def ServiceInfoPage(callback: CallbackQuery):
    id, sub_page, pg, sid = callback.data.split(":")[1:]
    res = one_table_info("services", "id", sid)
    if res != False:
        await callback.message.delete()
        await callback.message.answer(
            text=f"""<b><i>🗄 Kategoriya: {res[10]}</i>
                                      
📎 Xizmat: {res[2]}
💰 Narxi (1000 ta): {"{:.2f}".format((currency_calculator(api_currency, float(res[4]))) + (currency_calculator(api_currency, float(res[4])) / 100) * foiz)} so'm

<i>✔️ Buyurtma berish uchun pastdagi tugmani bosing.</i></b>""",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="✔️ Buyurtma berish", callback_data=f"zakaz-{sid}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="◀️ Orqaga",
                            callback_data=f"category:{id}:{sub_page}:{pg}",
                        )
                    ],
                ]
            ),
        )
    else:
        await callback.message.answer(
            text="<b>⚠️ Ushbu xizmat bazada topilmadi</b>", reply_markup=menu
        )


@router.callback_query(F.data.startswith("zakaz-"))
async def ZakazPage(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split("-")[1]
    res = one_table_info("services", "id", id)
    if res != False:
        await callback.message.delete()
        await callback.message.answer(
            text=f"""<b>◽️ Buyurtma miqdorini kiriting:
            
<i>⬇️ Minimal {res[5]} ta
⬆️ Maksimal {res[6]} ta.</i></b>""",
            reply_markup=back,
        )
        await state.update_data({"id": id})
        if res[3] == "Poll":
            rf = await state.set_state(AddZakazPoll.soni)
        elif res[3] == "Default":
            rf = await state.set_state(AddZakaz.soni)
    else:
        await callback.message.answer(
            "<b>⚠️ Xizmat haqida ma'lumot olishda xatolik yuz berdi.</b>",
            reply_markup=menu,
        )
        await state.clear()


@router.message(AddZakaz.soni)
async def ZakazPage2(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    res = one_table_info("services", "id", id)
    if res != False:
        if str(message.text).isdigit() == True:
            soni = int(message.text)
            if int(soni) >= int(res[5]) and int(soni) <= int(res[6]):
                res2 = one_table_info("api_key", "uid", admin)
                if res2 != False:
                    cv = await message.answer("<b>🕔 Iltimos kutib turing.</b>")
                    url1 = requests.get(
                        f"{res2[3]}/?key={res2[2]}&action=balance"
                    ).json()
                    t = (float(res[4]) / 1000) * int(message.text)
                    if t <= float(url1["balance"]):
                        res3 = one_table_info("users", "uid", message.chat.id)
                        if res != False:
                            if (float(res[4]) / 1000) * int(message.text) <= (currency_calculator(api_currency, float(res3[4]))):
                                await bot.delete_message(message.chat.id, cv.message_id)
                                await message.answer(
                                    text="<b>🔗 Xizmatni bajarish uchun kerakli URL manzilini yuboring.</b>",
                                    reply_markup=back,
                                )
                                rs = await state.set_state(AddZakaz.url)
                                await state.update_data({"soni": message.text})
                                await state.update_data(
                                    {"narx": ((float(res[4]) / 1000) * int(message.text)) + ((((float(res[4]) / 1000) * int(message.text)) / 100) * foiz)}
                                )
                            else:
                                await message.answer(
                            "<b>⚠️ Balansingizda yetarli mablag' mavjud emas.</b>",
                            reply_markup=menu,
                            
                        )
                                await state.clear()
                                                            
                        else:
                            await message.answer(
                            "<b>⚠️ Xizmatni bajarishda xatolik yuz beridi</b>",
                            reply_markup=menu,
                        )
                            await state.clear()
                    else:
                        await message.answer(
                            "<b>⚠️ Xizmatni bajarishda xatolik yuz beridi</b>",
                            reply_markup=menu,
                        )
                        await state.clear()
                else:
                    await message.answer(
                        "<b>⚠️ Xatolik yuz beridi</b>", reply_markup=menu
                    )
                    await state.clear()
            else:
                await message.answer(
                    text=f"""<b>⚠️ Buyurtma miqdorini kiriting:
                                 
<i>⬇️ Minimal {res[5]} ta
⬆️ Maksimal {res[6]} ta.</i></b>""",
                    reply_markup=back,
                )
        else:
            await message.answer(
                text=f"""<b>⚠️ Faqat raqamlardan foydalaning:
                                 
<i>⬇️ Minimal {res[5]} ta
⬆️ Maksimal {res[6]} ta.</i></b>""",
                reply_markup=back,
            )

    else:
        await message.answer(
            "<b>⚠️ Xizmat haqida ma'lumot olishda xatolik yuz berdi.</b>",
            reply_markup=menu,
        )
        await state.clear()


@router.message(AddZakaz.url)
async def ZakazPage3(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    soni = data.get("soni")
    narx = data.get("narx")
    res = one_table_info("services", "id", id)
    if res != False:
        if str(message.text).startswith("https://"):
            delete_table("order_temp", 'uid', message.chat.id)
            xc = AddOrderTemp(message.chat.id, id, soni, narx, message.text)
            if xc == True:
                vb = await message.answer(
                    text=f"""<b>◽️ Buyurtma haqida ma'lumotlar.</b>
                    
<i>🗄 Kategoriya: {res[10]}
📎 Xizmat: {res[2]}
💸 Narxi (1000 ta): {"{:.2f}".format((currency_calculator(api_currency, float(res[4]))) + (currency_calculator(api_currency, float(res[4])) / 100) * foiz)} so'm</i>

<b><i>⏺ Buyurtma miqdori: {soni} ta
💰 Buyurtma narxi: {"{:.2f}".format(currency_calculator(api_currency, float(narx)))} so'm</i></b>
""",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="✔️ Buyurtma berish", callback_data=f"addorder"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text="❌ Jarayonni bekor qilish",
                                    callback_data="cancel_order",
                                )
                            ],
                        ]
                    ),
                )
                # AddOrderDeleteMessage(message.chat.id, vb.message_id, vb.text)
                await state.clear()
            else:
                await message.answer(
                "<b>⚠️ Xatolik yuz berdi.</b>",
                reply_markup=menu,
            )
                await state.clear()
        else:
            await message.answer(
                "<b>⚠️ URL formati noto'gri.\n\nQaytadan urining</b>",
                reply_markup=back,
            )
    else:
        await message.answer(
            "<b>⚠️ Xizmat xaqida ma'lumotlarni olishda xatolik yuz berdi.</b>",
            reply_markup=menu,
        )
        await state.clear()

@router.callback_query(F.data == "addorder")
async def AddOrderx(callback: CallbackQuery):
    await callback.message.delete()
    temp = one_table_info("order_temp", 'uid', callback.message.chat.id)
    user_order = one_table_info('users', 'uid', callback.message.chat.id)
    if temp != False:
        res = one_table_info('services', 'id', temp[2])
        if res != False:
            res1 = one_table_info("api_key", 'uid', admin)
            if res1 != False:
                cv = await callback.message.answer("<b>🕔 Iltimos kutib turing.</b>")
                url = requests.get(f"{res1[3]}/?key={res1[2]}&action=services").json()
                if ('error' in url) == False:
                    order_add = requests.get(f"{res1[3]}/?key={res1[2]}&action=add&service={res[1]}&link={temp[5]}&quantity={temp[3]}").json()
                    if ('error' in order_add) == False:
                        if (float(res[4]) / 1000) * int(temp[3]) <= float(user_order[4]) / currency_calculator(api_currency, 1):
                            AddOrders(callback.message.chat.id, order_add['order'], res[0], res[1], res[2], currency_calculator(api_currency, float(temp[4])), temp[3], temp[5], '0')
                            UpdateUsersBalance(callback.message.chat.id, int(user_order[4]) - currency_calculator(api_currency, float(temp[4])))
                            await bot.delete_message(callback.message.chat.id, cv.message_id)
                            await callback.message.answer(f"<b>✅ Buyurtma berish muvaffaqiyatli amalga oshirildi, buyurtma ID raqami: {order_add['order']}</b>\n\n<i>ℹ️ Buyurtma haqida ma'lumotlarni '🛒 Buyurtmalarim' bo'limidan olishingiz mumkin.</i>", reply_markup=menu)
                            delete_table("order_temp", 'uid', callback.message.chat.id) 
                            UpdateUsersOrder(callback.message.chat.id, int(user_order[5]) + 1)
                        else:
                            await bot.delete_message(callback.message.chat.id, cv.message_id)
                            await callback.message.answer(
                                "<b>⚠️ Balansingizga yetarli mablag' mavjud emas.</b>",
                                reply_markup=menu,
                            )       
                            delete_table("order_temp", 'uid', callback.message.chat.id) 
                    else:
                        await bot.delete_message(callback.message.chat.id, cv.message_id)
                        await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
                        delete_table("order_temp", 'uid', callback.message.chat.id) 
                else:
                    await bot.delete_message(callback.message.chat.id, cv.message_id)
                    await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
                    delete_table("order_temp", 'uid', callback.message.chat.id)
            else:
                await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
                delete_table("order_temp", 'uid', callback.message.chat.id)
        else:
            await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
            delete_table("order_temp", 'uid', callback.message.chat.id)
            
    else:
        await callback.message.answer(
                "<b>⚠️ Xatolik yuz berdi.</b>",
                reply_markup=menu,
            )
        delete_table("order_temp", 'uid', callback.message.chat.id)

# POLL

@router.message(AddZakazPoll.soni)
async def ZakazPage2(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    res = one_table_info("services", "id", id)
    if res != False:
        if str(message.text).isdigit() == True:
            soni = int(message.text)
            if int(soni) >= int(res[5]) and int(soni) <= int(res[6]):
                res2 = one_table_info("api_key", "uid", admin)
                if res2 != False:
                    cv = await message.answer("<b>🕔 Iltimos kutib turing.</b>")
                    url1 = requests.get(
                        f"{res2[3]}/?key={res2[2]}&action=balance"
                    ).json()
                    t = (float(res[4]) / 1000) * int(message.text)
                    if t <= float(url1["balance"]):
                        res3 = one_table_info("users", "uid", message.chat.id)
                        if res != False:
                            if (float(res[4]) / 1000) * int(message.text) <= (currency_calculator(api_currency, float(res3[4]))):
                                await bot.delete_message(message.chat.id, cv.message_id)
                                await message.answer_photo(
                                    photo="https://telegra.ph/file/9f19686cb7ed220773b23.png",
                                    caption="<b>✔️ Sorovnoma qatnashuvchisining ismini yuboring.</b>",
                                    reply_markup=back,
                                )
                                rs = await state.set_state(AddZakazPoll.raqam)
                                await state.update_data({"soni": message.text})
                                await state.update_data(
                                    {"narx": ((float(res[4]) / 1000) * int(message.text)) + ((((float(res[4]) / 1000) * int(message.text)) / 100) * foiz)}
                                )
                            else:
                                await message.answer(
                            "<b>⚠️ Balansingizda yetarli mablag' mavjud emas.</b>",
                            reply_markup=menu,
                            
                        )
                                await state.clear()
                                                            
                        else:
                            await message.answer(
                            "<b>⚠️ Xizmatni bajarishda xatolik yuz beridi</b>",
                            reply_markup=menu,
                        )
                            await state.clear()
                    else:
                        await message.answer(
                            "<b>⚠️ Xizmatni bajarishda xatolik yuz beridi</b>",
                            reply_markup=menu,
                        )
                        await state.clear()
                else:
                    await message.answer(
                        "<b>⚠️ Xatolik yuz beridi</b>", reply_markup=menu
                    )
                    await state.clear()
            else:
                await message.answer(
                    text=f"""<b>⚠️ Buyurtma miqdorini kiriting:
                                 
<i>⬇️ Minimal {res[5]} ta
⬆️ Maksimal {res[6]} ta.</i></b>""",
                    reply_markup=back,
                )
        else:
            await message.answer(
                text=f"""<b>⚠️ Faqat raqamlardan foydalaning:
                                 
<i>⬇️ Minimal {res[5]} ta
⬆️ Maksimal {res[6]} ta.</i></b>""",
                reply_markup=back,
            )

    else:
        await message.answer(
            "<b>⚠️ Xizmat haqida ma'lumot olishda xatolik yuz berdi.</b>",
            reply_markup=menu,
        )
        await state.clear()
        
@router.message(AddZakazPoll.raqam)
async def ZakazPage2(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    res = one_table_info("services", "id", id)
    if res != False:
                res2 = one_table_info("api_key", "uid", admin)
                if res2 != False:
                        await message.answer(
                            text="<b>🔗 Xizmatni bajarish uchun kerakli URL manzilini yuboring.</b>",
                            reply_markup=back,
                        )
                        rs = await state.set_state(AddZakazPoll.url)
                        await state.update_data({"raqam": message.text})
                                                            
                else:
                    await message.answer(
                        "<b>⚠️ Xatolik yuz beridi</b>", reply_markup=menu
                    )
                    await state.clear()

    else:
        await message.answer(
            "<b>⚠️ Xizmat haqida ma'lumot olishda xatolik yuz berdi.</b>",
            reply_markup=menu,
        )
        await state.clear()


@router.message(AddZakazPoll.url)
async def ZakazPage3(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    soni = data.get("soni")
    narx = data.get("narx")
    raqam = data.get("raqam")
    res = one_table_info("services", "id", id)
    if res != False:
        if str(message.text).startswith("https://"):
            delete_table("order_temp", 'uid', message.chat.id)
            xc = AddOrderTemp(message.chat.id, id, f"{soni}--{raqam}", narx, message.text)
            if xc == True:
                vb = await message.answer(
                    text=f"""<b>◽️ Buyurtma haqida ma'lumotlar.</b>
                    
<i>🗄 Kategoriya: {res[10]}
📎 Xizmat: {res[2]}
💸 Narxi (1000 ta): {"{:.2f}".format((currency_calculator(api_currency, float(res[4]))) + (currency_calculator(api_currency, float(res[4])) / 100) * foiz)} so'm</i>

<b><i>⏺ Buyurtma miqdori: {soni} ta
💰 Buyurtma narxi: {"{:.2f}".format(currency_calculator(api_currency, float(narx)))} so'm</i></b>
""",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="✔️ Buyurtma berish", callback_data=f"addorderPoll"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text="❌ Jarayonni bekor qilish",
                                    callback_data="cancel_order",
                                )
                            ],
                        ]
                    ),
                )
                # AddOrderDeleteMessage(message.chat.id, vb.message_id, vb.text)
                await state.clear()
            else:
                await message.answer(
                "<b>⚠️ Xatolik yuz berdi.</b>",
                reply_markup=menu,
            )
                await state.clear()
        else:
            await message.answer(
                "<b>⚠️ URL formati noto'gri.\n\nQaytadan urining</b>",
                reply_markup=back,
            )
    else:
        await message.answer(
            "<b>⚠️ Xizmat xaqida ma'lumotlarni olishda xatolik yuz berdi.</b>",
            reply_markup=menu,
        )
        await state.clear()

@router.callback_query(F.data == "addorderPoll")
async def AddOrderx(callback: CallbackQuery):
    await callback.message.delete()
    temp = one_table_info("order_temp", 'uid', callback.message.chat.id)
    user_order = one_table_info('users', 'uid', callback.message.chat.id)
    if temp != False:
        action = str(temp[3]).split("--")
        soni = action[0]
        raqam = action[1]
        res = one_table_info('services', 'id', temp[2])
        if res != False:
            res1 = one_table_info("api_key", 'uid', admin)
            if res1 != False:
                cv = await callback.message.answer("<b>🕔 Iltimos kutib turing.</b>")
                url = requests.get(f"{res1[3]}/?key={res1[2]}&action=services").json()
                if ('error' in url) == False:
                    order_add = requests.get(f"{res1[3]}/?key={res1[2]}&action=add&service={res[1]}&link={temp[5]}&quantity={soni}&answer_number={raqam}").json()
                    if ('error' in order_add) == False:
                        if (float(res[4]) / 1000) * int(soni) <= float(user_order[4]) / currency_calculator(api_currency, 1):
                            await bot.delete_message(callback.message.chat.id, cv.message_id)
                            AddOrders(callback.message.chat.id, order_add['order'], res[0], res[1], res[2], currency_calculator(api_currency, float(temp[4])), temp[3], temp[5], '0')
                            UpdateUsersBalance(callback.message.chat.id, int(user_order[4]) - currency_calculator(api_currency, float(temp[4])))
                            await callback.message.answer(f"<b>✅ Buyurtma berish muvaffaqiyatli amalga oshirildi, buyurtma ID raqami: {order_add['order']}</b>\n\n<i>ℹ️ Buyurtma haqida ma'lumotlarni '🛒 Buyurtmalarim' bo'limidan olishingiz mumkin. Buyurtma bajarilganda yoki bekor qilinganda sizga xabar beramiz.</i>", reply_markup=menu)
                            delete_table("order_temp", 'uid', callback.message.chat.id) 
                            UpdateUsersOrder(callback.message.chat.id, int(user_order[5]) + 1)
                        else:
                            await bot.delete_message(callback.message.chat.id, cv.message_id)
                            await callback.message.answer(
                                "<b>⚠️ Balansingizga yetarli mablag' mavjud emas.</b>",
                                reply_markup=menu,
                            )       
                            delete_table("order_temp", 'uid', callback.message.chat.id) 
                    else:
                        await bot.delete_message(callback.message.chat.id, cv.message_id)
                        await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
                        delete_table("order_temp", 'uid', callback.message.chat.id) 
                else:
                    await bot.delete_message(callback.message.chat.id, cv.message_id)
                    await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
                    delete_table("order_temp", 'uid', callback.message.chat.id)
            else:
                await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
                delete_table("order_temp", 'uid', callback.message.chat.id)
        else:
            await callback.message.answer(
                "<b>⚠️ Xizmat ma'lumotlarini olishda xatolik yuzaga keldi, keyinroq urinib ko'ring.</b>",
                reply_markup=menu,
            )
            delete_table("order_temp", 'uid', callback.message.chat.id)
            
    else:
        await callback.message.answer(
                "<b>⚠️ Xatolik yuz berdi.</b>",
                reply_markup=menu,
            )
        delete_table("order_temp", 'uid', callback.message.chat.id)
