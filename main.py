import os
import glitchart
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Telegram-Glitch-Bot",
    bot_token = os.environ.get("BOT_TOKEN"),
    api_id = int(os.environ.get("API_ID")),
    api_hash = os.environ.get("API_HASH")
)


START_TEXT = """Merhaba {},
Ben fotograflarınıza glitch uygulayan Telegram botuyum.

Yapımcı @b4f2f"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Developer ', url='https://telegram.me/b4f2f'),
            InlineKeyboardButton('Blog', url='https://telegram.me/eGiblog')
        ]
    ]
)

PATH = os.environ.get("PATH", "./DOWNLOADS")


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.photo)
async def glitch_art(bot, update):
    download_path = PATH + "/" + str(update.from_user.id) + "/"
    download_location = download_path + "photo.jpg"
    message = await update.reply_text(
        text="`işleniyor...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        await update.download(
            file_name=download_location
        )
    except Exception as error:
        await message.edit_text(
            text=f"**HATA :** `{error}`\niletişim @b4f2f.",
            disable_web_page_preview=True
        )
        return 
    await message.edit_text(
        text="`glitche dönüştürülüyor...`"
    )
    try:
        glitch_art = glitchart.jpeg(download_location)
        await update.reply_photo(
            photo=glitch_art,
            caption=update.caption,
            quote=True
        )
        os.remove(download_location)
        os.remove(glitch_art)
    except Exception as error:
        await message.edit_text(
            text=f"**HATA :** `{error}`\niletişim @b4f2f.",
            disable_web_page_preview=True
        )
        return
    await message.delete()


Bot.run()
