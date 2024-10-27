# import requests
# import time

# from sqlite import AddNakCategory, AddNakServices, one_table_info

# url = requests.get("https://topsmm.uz/api/v2/?key=8bc44251c39a0fba149e3281846b9fca&action=services").json()
# url2 = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()

# # s = 0
# # l = list()

# # for i in url:
# #     if i['type'] == 'Default':
# #         if i['category'] not in l:
# #             l.append(i['category'])
            
# # for x in l:
# #     AddNakCategory(x)
    

# for i in url:
#     if i['type'] == 'Default':
#         res = one_table_info("category", "name", i['category'])
#         if res != False:
#             AddNakServices(i['service'], i['name'], i['type'], (((float(url2[2]["Rate"]) * float(i['rate'])) / 100) * 30) + (float(url2[2]["Rate"])) * float(i['rate']), i['min'], i['max'], i['dripfeed'], i['refill'], i['cancel'], i['category'], res[0])
#         else:
#             continue



# # print((((float(url2[2]["Rate"]) * float(1560.27)) / 100) * 30) + (float(url2[2]["Rate"])) * float(1560.27))


import asyncio
import os
import sys
import shutil
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import ContentType, InputMediaVideo
from aiogram.filters import Command
from moviepy.editor import VideoFileClip
import logging

API_TOKEN = '7002675047:AAFmTfpj9NE9be3f3_x8_1bfh5o5E5w79iI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

try:
    os.mkdir('files')
except:
    pass

@dp.message()
async def send_video(message: types.Message):
    try:
        url = message.text
        await message.reply_media_group([InputMediaVideo(media=url)])
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

# async def download_file(file_id: str, destination: str):
#     file = await bot.get_file(file_id)
#     await bot.download_file(file.file_path, destination)

# @router.message(F.content_type == ContentType.VIDEO)
# async def video_to_note_handler(message: types.Message):
#     r = await message.answer('⏳')
#     file_id = message.video.file_id
#     os.mkdir(f"files/{message.chat.id}")
#     await download_file(file_id, f"files/{message.chat.id}/video.mp4")
    
#     video_clip = VideoFileClip(f"files/{message.chat.id}/video.mp4")
#     video_clip.write_videofile(f"files/{message.chat.id}/output.mp4", codec="libx264", audio_codec="aac")
#     await bot.delete_message(message.from_user.id, r.message_id)
#     await message.answer_video_note(types.FSInputFile(f"files/{message.chat.id}/output.mp4"))
#     os.rmdir(f"files/{message.chat.id}")

# @router.message(F.content_type == ContentType.VIDEO_NOTE)
# async def note_to_video_handler(message: types.Message):
#     r = await message.answer('⏳')
#     file_id = message.video_note.file_id
#     await download_file(file_id, f"files/{message.chat.id}/video_note.mp4")
    
#     video_clip = VideoFileClip(f"files/{message.chat.id}/video_note.mp4")
#     video_clip.write_videofile(f"files/{message.chat.id}/output.mp4", codec="libx264", audio_codec="aac")
#     await bot.delete_message(message.from_user.id, r.message_id)
#     await message.answer_video(types.FSInputFile(f"files/{message.chat.id}/output.mp4"))
#     os.rmdir(f'files/{message.chat.id}')


dp.include_router(router)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == '__main__':
    dp.run_polling(bot)

