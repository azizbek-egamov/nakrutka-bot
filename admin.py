from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from button import *
from sqlite import *
from states import *
from functions import bot
import time
import requests
from config import admin

panel_dp = Router()


@panel_dp.message(Command("panel"), F.chat.id == 5668945618)
async def PanelPage(message: Message, state: FSMContext):
    await message.answer(
        "<b>Admin panelga xesh kelibsiz.</b>", reply_markup=admin_panel
    )
    await state.clear()


@panel_dp.message(F.text == "🗄 Admin panel", F.chat.id == 5668945618)
async def PanelPage(message: Message, state: FSMContext):
    await message.answer(
        "<b>Admin panelga xesh kelibsiz.</b>", reply_markup=admin_panel
    )
    await state.clear()


@panel_dp.callback_query(F.data == "panel")
async def CpanelPage(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer(
        "<b>Admin panelga xesh kelibsiz.</b>", reply_markup=admin_panel
    )
    await state.clear()


@panel_dp.message(F.text == "📊 Statistika")
async def Stats(message: Message):
    start_time = time.time()
    r = await bot.send_message(chat_id=message.chat.id, text="<b>1 soniya...</b>")
    end_time = time.time()
    send_time = end_time - start_time
    n = Statistic("users")
    await bot.delete_message(message.chat.id, r.message_id)
    await message.answer(
        text=f"""<b>💡 1 ta xabar yuborish tezligi: {'%.3f' % send_time} sekunnd.
        
👥 Foydalanuvchilar: {n} ta</b>""",
        reply_markup=orqaga,
    )


@panel_dp.message(F.text == "✉️ Xabar yuborish")
async def sendMess(message: Message):
    await message.answer(
        text="<b>◽️ Xabarni kimga yubormoqchisiz.</b>", reply_markup=send
    )


@panel_dp.callback_query(F.data == "all_message")
async def allMessage(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer(
        text="<b>Foydalanuvchilarga yuboriladigan xabar matnini kiriting.</b>",
        reply_markup=orqaga,
    )
    await state.set_state(AllUsersMessage.txt)


@panel_dp.message(AllUsersMessage.txt)
async def AllSend(message: Message, state: FSMContext):
    users = select_info("users")
    s = 0
    for x in users:
        if str(x[1]).startswith("-100"):
            continue
        else:
            s += 1
    xr = await message.answer(
        text=f"<b>{s} ta foydalanuvchiga xabar yuborish boshlandi.</b>"
    )
    for x in users:
        if str(x[1]).startswith("-100"):
            continue
        else:
            try:
                await bot.send_message(chat_id=f"{x[1]}", text=f"{message.text}")
            except:
                continue
    await message.answer(
        text=f"<b>{s} ta foydalanuvchiga xabar yuborish yakunlandi.</b>",
        reply_markup=orqaga,
    )
    await bot.delete_message(message.chat.id, xr.message_id)
    await state.clear()


@panel_dp.callback_query(F.data == "user_message")
async def UserMassage(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer(
        text="<b>Foydalanuvchi ID raqami yoki foydalanuvchi nomini kiriting <i>(@ bilan)</i>.</b>",
        reply_markup=orqaga,
    )
    await state.set_state(UserMess.user)


@panel_dp.message(UserMess.user)
async def UserSearch(message: Message, state: FSMContext):
    if message.text.isdigit():
        r = table_info("users", "uid", message.text)
        if r != False:
            for x in r:
                await state.update_data({"uid": x[1]})
                break
            await message.answer(
                text="Foydalanuvchiga yuboriladigan xabar matnini kiriting.",
                reply_markup=orqaga,
            )
            await state.set_state(UserMess.txt)
        else:
            await message.answer(
                text="<b>Foydalanuvchi topilmadi</b>", reply_markup=orqaga
            )
    elif message.text.startswith("@"):
        rep = message.text.replace("@", "")
        r = table_info("users", "username", rep)
        if r != False:
            for x in r:
                await state.update_data({"uid": x[1]})
                break
            await message.answer(
                text="Foydalanuvchiga yuboriladigan xabar matnini kiriting.",
                reply_markup=orqaga,
            )
            await state.set_state(UserMess.txt)
        else:
            await message.answer(
                text="<b>Foydalanuvchi topilmadi</b>", reply_markup=orqaga
            )
    else:
        await message.answer(
            text="<b>⚠️ Foydalanuvchi ID raqami yoki foydalanuvchi nomini kiriting <i>(@ bilan)</i>.</b>",
            reply_markup=orqaga,
        )


@panel_dp.message(UserMess.txt)
async def SendUserMess(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("uid")
    await bot.send_message(chat_id=f"{id}", text=f"{message.text}")
    await message.answer(
        text="<b>Xabaringiz foydalanuvchiga yuborildi</b>", reply_markup=admin_panel
    )
    await state.clear()


@panel_dp.message(F.text == "〽️ API kalit")
async def APIKEY(message: Message):
    res = table_info("api_key", "uid", admin)
    if res != False:
        btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="ℹ️ Kalit ma'lumotlari", callback_data="key_info"
                    ),
                    InlineKeyboardButton(
                        text="🗑 Kalitni olib tashlash", callback_data="key_delete"
                    ),
                ]
            ]
        )
        await message.answer(text="◽️ Kearkli bo'limni tanlang", reply_markup=btn)
    else:
        btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="➕ Kalit qo'shish", callback_data="key_add"
                    ),
                ]
            ]
        )
        await message.answer(text="◽️ Kearkli bo'limni tanlang", reply_markup=btn)


@panel_dp.callback_query(F.data == "key_info")
async def APIKEYINFO(callback: CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    res = table_info("api_key", "uid", admin)
    if res != False:
        for i in res:
            url = requests.get(f"{i[3]}/?key={i[2]}&action=balance").json()
            if ("error" in url) == False:
                await callback.message.answer(
                    text=f"""ℹ️ API kalit haqida ma'lumotlar:

🔗 Kalit URL si: {i[3]},
🔑 Kalit: {i[2]}.

💰 Kalit balansi: {url["balance"]}""",
                )
            else:
                await callback.message.answer(
                    text=f"""ℹ️ API kalit haqida ma'lumotlar:

🔗 Kalit URL si: {i[3]},
🔑 Kalit: {i[2]}.

⚠️ Bu kalit yaroqsiz uni almashtiring.""",
                )


@panel_dp.callback_query(F.data == "key_add")
async def ApiKeyAdd(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="✔️ Kalit URL sini yuboring.\n\nMasalan: <code>https://topsmm.uz/api/v2</code>.",
        reply_markup=aorqaga,
    )
    await state.set_state(AddApiKey.url)


@panel_dp.message(AddApiKey.url)
async def ApiKeyAddUrl(message: Message, state: FSMContext):
    if str(message.text).startswith("https://") and str(message.text).endswith(
        ("v2", "v1", "v3")
    ):
        try:
            url = requests.get(f"{message.text}").json()
        except:
            await message.answer(
                text="⚠️ Yaroqsiz URL, \n\nQaytadan urining",
                reply_markup=aorqaga,
            )
        if "error" in url:
            await message.answer(text="🔑 API kalitni yuboring.", reply_markup=aorqaga)
            await state.set_state(AddApiKey.key)
            await state.update_data({"url": message.text})
        else:
            await message.answer(
                text="⚠️ Yaroqsiz URL, \n\nQaytadan urining",
                reply_markup=aorqaga,
            )
    else:
        await message.answer(
            text="⚠️ Kalit URL sini yuboring.\n\nMasalan: <code>https://topsmm.uz/api/v2</code>.",
            reply_markup=aorqaga,
        )


@panel_dp.message(AddApiKey.key)
async def ApiKeyAddKey(message: Message, state: FSMContext):
    data = await state.get_data()
    link = data.get("url")
    if message.text:
        x = requests.get(f"{link}/?key={message.text}&action=balance").json()
        print(f"{link}/?key={message.text}&action=balance")
        print(x)
        if ("error" in x) == False:
            AddApi(message.chat.id, message.text, link)
            await message.answer(
                text=f"✔️ Kalit botga muvaffaqiyatli ulandi.\n\n💸 Kalit balansi: {x['balance']}",
                reply_markup=admin_panel,
            )
            await state.clear()
        else:
            await message.answer(
                text="⚠️ Yaroqsiz kalit,\n\n Qaytadan urinib ko'ring",
                reply_markup=aorqaga,
            )


@panel_dp.callback_query(F.data == "key_delete")
async def DelApiKey(callback: CallbackQuery):
    res = delete_table("api_key", "uid", admin)
    await callback.message.delete()
    if res == True:
        await callback.message.answer(
            "🗑 Kalit muvaffaqiayatli olib tashalndi", reply_markup=admin_panel
        )
    else:
        await callback.message.answer(
            "❌ Kalitni olib tashlashda xatolik yuz berdi", reply_markup=admin_panel
        )


@panel_dp.message(F.text == "🗂 Xizmatlar")
async def ServicePage(message: Message):
    res = select_info("services")

    if res == False:
        btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬇️ Xizmatlarni yuklab olish",
                        callback_data="servicess_download",
                    )
                ]
            ]
        )
        await message.answer(
            "🗄 Karakli bo'limni tanlang:\n\n<i>Esalatma: xizmatlarni yuklab olsangiz dastur o'zi saytdagi kerakli barcha xizmatlarni yuklab oladi va kategoriyalarga ajratadi. Jarayon yakunlanguncha xatolik bo'lmasligi uchun botni o'chirib qo'yishingiz kerak</i>",
            reply_markup=btn,
        )
    else:
        btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🗑 Xizmatlarni o'chirib tashlash",
                        callback_data="servicess_delete",
                    )
                ]
            ]
        )
        await message.answer(
            "🗄 Karakli bo'limni tanlang:\n\n<i>Esalatma: xizmatlarni o'chirib tashlasangiz dastur qo'shilgan barcha kategoriyalar va xizmatlarni yo'q qiladi Jarayon yakunlanguncha xatolik bo'lmasligi uchun botni o'chirib qo'yishingiz kerak</i>",
            reply_markup=btn,
        )


@panel_dp.callback_query(F.data.startswith("servicess_"))
async def ServiceSettings(callback: CallbackQuery):
    status = callback.data.split("_")[1]
    if status == "download":
        await callback.message.delete()
        mn = await callback.message.answer(
            "⬇️ Xizmatlarni yuklab olish boshlandi\n\n<i>Jarayon bir necha soniya vaqt olishi mumkin</i>"
        )
        res = select_info("api_key")

        for i in res:
            url = requests.get(f"{i[3]}/?key={i[2]}&action=services").json()
            print(f"{i[3]}/?key={i[2]}&action=services")
            break
        if "error" in url:
            await bot.delete_message(callback.message.chat.id, mn.message_id)
            await callback.message.answer(
                "🔑⚠️ Api kalit yaroqsiz, uni almashtiring", reply_markup=admin_panel
            )
        else:
            o = True
            try:
                l = list()

                for i in url:
                    if i["type"] == "Default" or i["type"] == "Poll":
                        if i["category"] not in l:
                            l.append(i["category"])

                for x in l:
                    AddNakCategory(x)

                for k in url:
                    if k["type"] == "Default" or k["type"] == "Poll":
                        ress = one_table_info("category", "name", k["category"])
                        if ress != False:
                            AddNakServices(
                                k["service"],
                                k["name"],
                                k["type"],
                                k['rate'],
                                k["min"],
                                k["max"],
                                k["dripfeed"],
                                k["refill"],
                                k["cancel"],
                                k["category"],
                                ress[0],
                            )
                        else:
                            continue
            except Exception as e:
                print(e)
                o = False
            if o == False:
                await bot.delete_message(callback.message.chat.id, mn.message_id)
                dalete_info("category")
                dalete_info("services")
                await callback.message.answer(
                    "⚠️ Yuklab olishda xatolik yuz berdi", reply_markup=admin_panel
                )
            else:
                await bot.delete_message(callback.message.chat.id, mn.message_id)
                await callback.message.answer(
                    "✔️ Xizmatlarni yuklab olish muvaffaqiyatli amalga oshirildi.",
                    reply_markup=admin_panel,
                )
    elif status == "delete":
        dalete_info("category")
        dalete_info("services")
        await callback.message.delete()
        await callback.message.answer(
            "🗑 Xizmatlar o'chirib tashlandi", reply_markup=admin_panel
        )


@panel_dp.message(F.text == "💳 To'lov tizimlari")
async def AdPayPlusPage(message: Message):
    res = select_info("pay_cards")
    if res != False:
        btn = InlineKeyboardBuilder()
        for i in res:
            btn.add(
                InlineKeyboardButton(
                    text=f"{i[1]}", callback_data=f"del_paycard-{i[0]}"
                )
            )
        btn.add(InlineKeyboardButton(text="➕ Qo'shish", callback_data="add_paycard"))
        btn.adjust(1)

        await message.answer(
            text="<b>💳 Barcha to'lov tizimlari ro'yhati.</b>\n\n<i>🗑 Keraksiz to'lov tizimi ustiga bosib uni o'chirib tashlashingiz mumkin.</i>",
            reply_markup=btn.as_markup(),
        )
    else:
        await message.answer(
            text="<b>💁🏻‍♂️ To'lov tizimlari mavjud emas</b>",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="➕ Qo'shish", callback_data="add_paycard"
                        )
                    ]
                ]
            ),
        )


@panel_dp.callback_query(F.data == "add_paycard")
async def AddPayCard(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="<b>◽️ Hamyon nomini yuboring.</b>", reply_markup=aorqaga
    )
    await state.set_state(AddPayCards.name)


@panel_dp.message(AddPayCards.name)
async def AddPayCard2(message: Message, state: FSMContext):
    if message.text:
        await message.answer(
            text=f"{message.text} <b>qabul qilindi endi hamyon raqamini yuboring.</b>",
            reply_markup=aorqaga,
        )
        await state.update_data({"name": message.text})
        await state.set_state(AddPayCards.card)


@panel_dp.message(AddPayCards.card)
async def AddPayCard3(message: Message, state: FSMContext):
    txt = message.text
    if txt:
        if str(txt).isdigit():
            await message.answer(
                text=f"<b>Qabul qilindi endi to'lov haqida ma'lumot kiriting.</b>",
                reply_markup=aorqaga,
            )
            await state.update_data({"card": message.text})
            await state.set_state(AddPayCards.info)
        else:
            await message.answer(
                "<b>⚠️ Faqat raqamlardan foydalaning</b>", reply_markup=aorqaga
            )


@panel_dp.message(AddPayCards.info)
async def AddPayCard3(message: Message, state: FSMContext):
    txt = message.text
    if txt:
        data = await state.get_data()
        name = data.get("name")
        card = data.get("card")
        AddPayments(name, card, txt)
        await message.answer(
            text=f"<b>✅ To'lov hamyoni muvaffaqiyatli qo'shildi</b>",
            reply_markup=admin_panel,
        )
        await state.clear()


@panel_dp.callback_query(F.data.startswith("del_paycard-"))
async def delPayCard(callback: CallbackQuery):
    id = callback.data.split("-")[1]
    delete_table("pay_cards", "id", id)
    await callback.message.delete()
    await callback.message.answer("<b>🗑 Hamyon muvaffaqiyatli olib tashlandi</b>")


@panel_dp.message(F.text == "👤 Foydalanuvchini boshqarish")
async def UserControl(message: Message, state: FSMContext):
    await message.answer(
        text="<b>Foydalanuvchi ID raqamini kiriting.</b>", reply_markup=aorqaga
    )
    await state.set_state(usercontrol.id)


@panel_dp.message(usercontrol.id)
async def usercontrol2(message: Message, state: FSMContext):
    res = one_table_info("users", "uid", message.text)
    print(res)
    if res != False:
        if str(res[8]) == 'false':
            btn = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🔒 Banlash", callback_data=f"ban-ban-{message.text}")
                    ],
                    [
                        InlineKeyboardButton(
                            text="➕ Pul qo'shish", callback_data=f"plus-{message.text}"
                        ),
                        InlineKeyboardButton(
                            text="➖ Pul ayirish", callback_data=f"minus-{message.text}"
                        ),
                    ]
                ]
            ),
        elif str(res[8]) == 'true':
            btn = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🔓 Bandan olish", callback_data=f"ban-unban-{message.text}")
                    ],
                    [
                        InlineKeyboardButton(
                            text="➕ Pul qo'shish", callback_data=f"plus-{message.text}"
                        ),
                        InlineKeyboardButton(
                            text="➖ Pul ayirish", callback_data=f"minus-{message.text}"
                        ),
                    ]
                ]
            ),
        await message.answer(
            text=f"""<b>✔️ Foydalanuvchi topildi</b>
 
<i><b>👤 Foydalanuvchi: {res[2]}           
🆔 ID raqami: {res[1]}
▫️ Username: {'Mavjud emas' if res[3] == None else '@' + str(res[3])}
💸 Balansi: {res[4]} so'm
💰 Kiritgan pullari: {res[6]} so'm
🗂 Buyurtmalar: {res[5]} ta
👤 Takliflar: {res[7]}ta</b></i>
""",
            reply_markup=btn
        )
        await state.clear()
    else:
        await message.answer(
            text="<b>Foydalanuvchi topilmadi\n\nQaytadan urining</b>",
            reply_markup=aorqaga,
        )


@panel_dp.callback_query(F.data.startswith('plus-'))
async def BalancePlusPage(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split('-')[1]
    await callback.message.delete()
    await callback.message.answer(
        text="<b>Foydalanuvchi balansiga qancha miqdorda pul qo'shmoqchisiz.</b>", 
        reply_markup=aorqaga
    )
    await state.update_data({'id': id})
    await state.set_state(userPlus.count)
    
@panel_dp.message(userPlus.count)
async def  UserPlusPage2(message: Message, state: FSMContext):
    if str(message.text).isdigit():
        data = await state.get_data()
        id = data.get('id')
        user = one_table_info('users', 'uid', id)
        UpdateUsersBalance(id, float(user[4] + float(message.text)))
        await message.answer(f'<b>✔️ Foydalanuvchi balansiga {message.text} so\'m qo\'shildi</b>', reply_markup=admin_panel)
        await bot.send_message(
            chat_id=id,
            text=f"<b>Sizning balansingizga {message.text} so'm qo'shildi</b>"
        )
        await state.clear()
    else:
        await message.answer(
            text="<b>⚠️ Faqat raqamlardan foydalaning</b>",
            reply_markup=aorqaga
        )
        
@panel_dp.callback_query(F.data.startswith('minus-'))
async def BalancePlusPage(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split('-')[1]
    await callback.message.delete()
    await callback.message.answer(
        text="<b>Foydalanuvchi balansidan qancha miqdorda pul olib tashlamoqchisiz.</b>", 
        reply_markup=aorqaga
    )
    await state.update_data({'id': id})
    await state.set_state(userMinus.count)
    
@panel_dp.message(userMinus.count)
async def  UserPlusPage2(message: Message, state: FSMContext):
    if str(message.text).isdigit():
        data = await state.get_data()
        id = data.get('id')
        user = one_table_info('users', 'uid', id)
        UpdateUsersBalance(id, float(user[4] - float(message.text)))
        await message.answer(f'<b>✔️ Foydalanuvchi balansidan {message.text} so\'m olib tashlandi</b>', reply_markup=admin_panel)
        await bot.send_message(
            chat_id=id,
            text=f"<b>Sizning balansingizdan {message.text} so'm olib tashlandi</b>"
        )
        await state.clear()
    else:
        await message.answer(
            text="<b>⚠️ Faqat raqamlardan foydalaning</b>",
            reply_markup=aorqaga
        )