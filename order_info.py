from sqlite import *
from config import admin
from functions import bot
import requests
import asyncio

async def OrderInfo():
    while True:
        orders = select_info("orders")
        api = one_table_info("api_key", "uid", admin)

        if api != False:
            if orders != False:
                for i in orders:
                    if str(i[9]) == "0":
                        CHECK_URL = f"{api[3]}/?key={api[2]}&action=status&order={i[2]}"
                        try:
                            res = requests.get(CHECK_URL).json()
                            if res["status"] == "Completed":
                                await bot.send_message(
                                    chat_id=f"{i[1]}",
                                    text=f"""<b>✅ Buyurtmangiz bajarildi
                                
🆔 Buyurtma ID raqami: {i[2]}
💰 Narxi: {"{:.2f}".format(i[6])} so'm
🔄 Miqdor: {i[7]}
✔️ Holati: Bajarilgan.</b>""",
                                )
                                UpdateOrderSendStatus(i[0], "1")
                            elif res["status"] == "Canceled":
                                await bot.send_message(
                                    chat_id=f"{i[1]}",
                                    text=f"""<b>❌ Buyurtmangiz bajarilmadi
                                    
🆔 Buyurtma ID raqami: {i[2]}
💰 Narxi: {"{:.2f}".format(i[6])} so'm
🔄 Miqdor: {i[7]}
❌ Holati: Bekor qilingan.</b>""",
                                )
                                UpdateOrderSendStatus(i[0], "1")
                            elif res["status"] == "Partial":
                                await bot.send_message(
                                    chat_id=f"{i[1]}",
                                    text=f"""<b>◽️ Buyurtmangiz qisman bajarildi
                                    
🆔 Buyurtma ID raqami: {i[2]}
💰 Narxi: {"{:.2f}".format(i[6])} so'm
🔄 Miqdor: {i[7]}
◽️ Holati: Qisman bajarilgan.</b>""",
                                )
                                UpdateOrderSendStatus(i[0], "1")
                            else:
                                continue
                        except requests.exceptions.RequestException as e:
                            print(f"Error fetching order status: {e}")
                        except ValueError:
                            print("Invalid response received")
                    else:
                        continue
        await asyncio.sleep(60)