from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def webapp_kbd(webapp_url: str):
    wa_kbd_builder = ReplyKeyboardBuilder()
    wa_kbd_builder.button(text='Choose character', web_app=WebAppInfo(
        url=webapp_url))
    return wa_kbd_builder.as_markup()
