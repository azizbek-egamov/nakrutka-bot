# START CODING

from functions import *
from admin import *
from services import *
from orders import *
from payment import *



async def joinchat(user_id: int) -> bool:
    btn = InlineKeyboardBuilder()
    is_subscribed = True

    for ch in channel:
        try:
            user_status = await bot.get_chat_member(f"@{ch}", user_id)
        except Exception as e:
            logging.error(f"Error checking user status in channel {ch}: {e}")
            continue

        if user_status.status not in ["creator", "administrator", "member"]:
            btn.add(
                InlineKeyboardButton(text="Obuna bo'lish", url=f"https://t.me/{ch}")
            )
            is_subscribed = False
    
    btn.add(InlineKeyboardButton(text="✅ Tekshirish", callback_data="result"))
    btn.adjust(1)

    if not is_subscribed:
        await bot.send_message(
            chat_id=user_id, text="<b>✔️ Bot xizmatlaridan foydalanish uchun pastdagi kanallarga obuna bo'lishingiz kerak.</b>", reply_markup=btn.as_markup()
        )
        return False
    return True


# async def phone_check(update: Update) -> bool:
#     if isinstance(update, Message):
#         user_id = update.from_user.id
#     elif isinstance(update, CallbackQuery):
#         user_id = update.from_user.id

#     cursor.execute("SELECT * FROM phone WHERE uid=?", (user_id,))
#     result = cursor.fetchall()

#     if result is None:
#         await bot.send_message(
#             chat_id=user_id,
#             text="<b>'📲 Raqamni yuborish' tugmasini bosgan holda telefon raqamingizni yuboring.</b>",
#             reply_markup=ReplyKeyboardMarkup(
#                 keyboard=[
#                     [KeyboardButton(text="📲 Raqamni yuborish", request_contact=True)]
#                 ],
#                 resize_keyboard=True,
#             ),
#         )
#         return False
#     return True

# @dp.message(F.contact)
# async def handle_contact(message: types.Message):
#     user_id = message.from_user.id
#     phone_number = message.contact.phone_number

#     if message.contact.user_id == user_id:
#         cursor.execute(
#             "INSERT OR IGNORE INTO phone (uid, number) VALUES (?, ?)",
#             (user_id, phone_number),
#         )
#         conn.commit()

#         await message.answer(
#             text=f"""<b>👋 Salom {message.chat.full_name}.

# <i>🤖 Bu bot orqali siz o'zingiz yashab turgan shahar yoki tumanning namoz vaqti ma'lumotlarini bilib borishingiz mumkin.</i></b>""",
#             reply_markup=menu,
#         )
#     else:
#         await message.answer("Faqat o'zingizni raqamingizni yuboring")


# # @dp.message(CommandStart())
# # async def startbot(message: Message, event: Update):
# #     if await joinchat(event) == True:
# #         if await phone_check(message) == True:
# #             await message.answer(
# #                 text=f"""<b>👋 Salom {message.chat.full_name}.

# # <i>🤖 Bu bot orqali siz o'zingiz yashab turgan shahar yoki tumanning namoz vaqti ma'lumotlarini bilib borishingiz mumkin.</i></b>""",
# #                 reply_markup=menu,
# #             )


@dp.message(CommandStart())
async def startbot(message: Message, state: FSMContext):
    args = message.text.split()
    uid = message.chat.id
    if len(args) > 1:
        if str(args[1]) != str(uid):
            res = one_table_info("users", "uid", uid)
            print(res)
            if res == False:
                r = AddRef(uid, args[1])
                print(r, "salom")
                if await joinchat(uid) == True:
                    delete_table("referal", "uid", uid)
                    await bot.send_message(
                        chat_id=args[1],
                        text=f"<b>➕ Siz botga {message.chat.full_name} ni taklif qildingiz va balansingizga {referal} so'm qo'shildi.</b>",
                    )
                    add_information(
                        uid, message.chat.full_name, message.chat.username, 0, 0, 0, 0, 'false'
                    )

            if await joinchat(uid):
                await message.answer(
                    text=f"""<b>👋 Salom {message.chat.full_name}.</b>""",
                    reply_markup=menu,
                )
    else:
        add_information(uid, message.chat.full_name, message.chat.username, 0, 0, 0, 0, 'false')
        if await joinchat(uid):
            await message.answer(
                text=f"""<b>👋 Salom {message.chat.full_name}.</b>""",
                reply_markup=menu,
            )
            delete_table("order_temp", "uid", message.chat.id)
            await state.clear()
            
    print(await CheckChannel("@visualcoders_chat"))
        


@dp.callback_query(F.data == "result")
async def resu(callback: CallbackQuery, state: FSMContext):
    uid = callback.message.chat.id
    if await joinchat(uid):
        res = one_table_info("referal", "uid", uid)
        if res != False:
            add_information(
                uid,
                callback.message.chat.full_name,
                callback.message.chat.username,
                0,
                0,
                0,
                0,
                'false'
            )
            user_info = one_table_info("users", "uid", res[2])
            UpdateRaferalCount(res[2], int(user_info[7]) + 1)
            delete_table("referal", "uid", uid)

            await bot.send_message(
                chat_id=res[2],
                text=f"<b>➕ Siz botga {callback.message.chat.full_name} ni taklif qildingiz va balansingizga {referal} so'm qo'shildi.</b>",
            )

            await bot.delete_message(
                callback.message.chat.id, callback.message.message_id
            )
            await callback.message.answer(
                text=f"""<b>👋 Salom {callback.message.chat.full_name}.</b>""",
                reply_markup=menu,
            )
            delete_table("order_temp", "uid", callback.message.chat.id)
            await state.clear()

        else:

            await bot.delete_message(
                callback.message.chat.id, callback.message.message_id
            )
            await callback.message.answer(
                text=f"""<b>👋 Salom {callback.message.chat.full_name}.</b>""",
                reply_markup=menu,
            )
            delete_table("order_temp", "uid", callback.message.chat.id)
            await state.clear()


@dp.message(F.text == "◀️ Orqaga")
async def startbot(message: Message, state: FSMContext):
    uid = message.chat.id
    if await joinchat(uid):
        await message.answer(
            text=f"""<b>🏘 Asosiy menyudasiz.</b>""",
            reply_markup=menu,
        )
        delete_table("order_temp", "uid", message.chat.id)
        await state.clear()


@dp.callback_query(F.data == "cancel_order")
async def resu(callback: CallbackQuery, state: FSMContext):
    uid = callback.message.chat.id
    if await joinchat(uid):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.answer(
            text=f"""<b>🏘 Asosiy menyudasiz.</b>""",
            reply_markup=menu,
        )
        delete_table("order_temp", "uid", callback.message.chat.id)
        await state.clear()


@dp.message(F.text == "💵 Hisobim")
async def refPage(message: Message):
    uid = message.chat.id
    if await joinchat(uid):
        user = one_table_info("users", "uid", uid)
        await message.answer(
            text=f"""<b>🆔 ID raqamingiz:</b> <code>{uid}</code>
            
<i>💰 Balansingiz: {"{:.2f}".format(float(user[4]))} so'm
📎 Takliflar: {user[7]} ta
📦 Buyurtmalar: {user[5]} ta

💳 Botga kiritilgan pullar: {"{:.2f}".format(float(user[6]))} so'm</i>"""
        )


@dp.message(F.text == "💰 Pul ishlash")
async def MakeMoney(message: Message):
    if await joinchat(message.chat.id):
        await message.answer(
            text="<b>💰 Kerakli bo'limni tanlang.</b>",
            reply_markup=make_money
        )
        
@dp.callback_query(F.data == "ref")
async def accountPage(callback: CallbackQuery):
    uid = callback.message.chat.id
    if await joinchat(uid):
        await callback.message.delete()
        await callback.message.answer(
            text=f"""<b>🗣 Sizning taklif havolangiz.
            
<code>https://t.me/{await botuser()}?start={uid}</code>

💸 Har bitta taklif uchun {referal} so'm beriladi.</b>""",
reply_markup=menu
        )

@dp.callback_query(F.data == "group")
async def accountPage(callback: CallbackQuery):
    uid = callback.message.chat.id
    if await joinchat(uid):
        await callback.message.delete()
        await callback.message.answer(
            text=f"""<b>✔️ Guruhga odam qo'shish:
            
👇🏻 Pastdagi tugma orqali guruhga kiriting va kontaktingizdan bir nechta odam qo'shing. Har bir qo'shgan odamingiz uchun {group_narx} so'm balansingizga qo'shiladi.</b>""",
reply_markup=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Guruhga kirish", url=group_url)]
    ]
)
        )
        
class NewChatMembersFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.new_chat_members is not None and str(message.chat.id) == group_id

@dp.message(NewChatMembersFilter())
async def new_member_handler(message: Message):
    new_members = message.new_chat_members
    print(new_members)
    print(message.from_user.id)
    for member in new_members:
        res = one_table_info('users', 'uid', message.from_user.id)
        print(res)
        if res != False:
            user_info = f"<b>✔️ Siz guruhga {member.full_name} ni qo'shdingiz va balansingizga {group_narx} so'm qo'shildi</b>"
            UpdateUsersBalance(message.from_user.id, float(res[4]) + float(group_narx))
            if message.from_user.id != member.id:
                await bot.send_message(message.from_user.id, user_info)


@dp.message(F.text == "📨 Murojaat")
async def support(message: Message, state: FSMContext):
    uid = message.chat.id
    if await joinchat(uid):
        await message.answer(
            text="<b>📨 Xabarni kriting.</b>",
            reply_markup=back,
        )
        await state.set_state(Support.text)


@dp.message(Support.text)
async def Support2(message: Message, state: FSMContext):
    if message.text:
        r = await CheckChannel(message.chat.id)
        await message.answer(
            text="<b>📨 Xabaringiz adminga yuborildi, tez orada javob olasiz.</b>",
            reply_markup=menu,
        )
        await bot.send_message(
            chat_id=admin,
            text=f"""<b>📨 Sizga murojaat kelib tushdi.
            
🆔 Raqami: {r.id}
👤 Ismi: {r.first_name}
🔗 Useri: {'Mavjud emas' if r.username is None else '@' + r.username}

💬 Xabari:</b>

<i>{message.text}</i>""",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="💬 Javob qaytarish", callback_data=f"senm-{r.id}"
                        ),
                        InlineKeyboardButton(
                            text="❌ Etiborsiz qoldirish", callback_data="delete"
                        ),
                    ]
                ]
            ),
        )
        await state.clear()


@dp.callback_query(F.data.startswith("senm-"))
async def SendUserGa(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("<b>Xabarni kiriting</b>", reply_markup=back)
    await state.update_data({"id": callback.data.split("-")[1]})
    await state.set_state(UserSendSupport.text)


@dp.message(UserSendSupport.text)
async def SendUserga2(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get("id")
    if message.text:
        await bot.send_message(
            chat_id=id,
            text=f"<b>✔️ Admindan xabaringizga javob xati keldi.</b>\n\n<i>💬 Xabar: {message.text}</i>",
        )
        await message.answer("<b>Xabar yuborildi</b>", reply_markup=menu)
        await state.clear()


async def main() -> None:
    dp.include_routers(panel_dp)
    dp.include_routers(services_dp)
    dp.include_routers(orders_dp)
    dp.include_routers(payment_dp)
    asyncio.create_task(OrderInfo())
    

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except:
        print("Jarayon yakunlandi")
