import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import BaseFilter

TOKEN = "7002675047:AAFmTfpj9NE9be3f3_x8_1bfh5o5E5w79iI"
bot = Bot(token=TOKEN)
group_id = '-1002238635651'

dp = Dispatcher()

class NewChatMembersFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.new_chat_members is not None and str(message.chat.id) == group_id

@dp.message(NewChatMembersFilter())
async def new_member_handler(message: Message):
    new_members = message.new_chat_members
    for member in new_members:
        user_info = f"Siz guruhga yangi foydalanuvchi qo'shdingiz:\nID: {member.id}\nIsmi: {member.full_name}\nUsername: @{member.username if member.username else 'None'}"
        
        if message.from_user.id != member.id:
            await bot.send_message(message.from_user.id, user_info)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except:
        print("Jarayon yakunlandi")


# import yt_dlp

# def download_video(video_url):
#     ydl_opts = {
#         'format': 'bestvideo+bestaudio/best',
#         'outtmpl': '%(title)s.%(ext)s'
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#         print("Video yuklandi")

# def download_audio(video_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': '%(title)s.%(ext)s',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#         print("Audio yuklandi")

# # Replace 'YOUR_VIDEO_URL' with the actual video URL you want to download
# video_url = 'https://youtu.be/1FZ7DbQwVcw?list=RDGMEM6ijAnFTG9nX1G-kbWBUCJAVM1FZ7DbQwVcw'

# download_video(video_url)
# download_audio(video_url)
