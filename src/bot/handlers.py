from contextlib import suppress
from pprint import pprint

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from amplitude import Amplitude, BaseEvent

from src.bot.gpt_api import fetch_completion
from src.bot.keyboards import webapp_kbd
from src.bot.services import Repository
from src.bot.states import Messaging

router = Router()


@router.message(CommandStart())
async def msg_echo(message: types.Message, ampl: Amplitude, db: Repository, webapp: str):
    ampl.track(BaseEvent(
        event_type='started',
        user_id=f'{message.from_user.id}',
    ))
    await db.save_user(message.from_user)
    await message.answer(
        text='Hello! This bot is created to make possible '
             'communication with great characters',
        reply_markup=webapp_kbd(webapp))


@router.message(Command(commands='menu'))
async def menu_handler(message: types.Message, webapp: str):
    await message.answer('Please choose a character!',
                         reply_markup=webapp_kbd(webapp))


@router.message(F.web_app_data)
async def handle_data(message: types.Message, db: Repository, ampl: Amplitude, state: FSMContext):
    greeting = await db.get_char_greetings(message.web_app_data.data)
    await message.answer(greeting)
    await db.choose_character(message.from_user.id, message.web_app_data.data)
    ampl.track(BaseEvent(
        event_type='char_choice',
        user_id=f'{message.from_user.id}'
    ))
    await state.set_state(Messaging.message_inc)


@router.message(Messaging.message_inc)
async def handle_request_by_char(message: types.Message, ampl: Amplitude, db: Repository, state: FSMContext):
    conv_id = await db.write_message(message.from_user.id, message.text)
    ampl.track(BaseEvent(
        event_type='user_req',
        user_id=f'{message.from_user.id}'
    ))
    prompt = await db.get_prompt(message.from_user.id)
    await state.set_state(Messaging.message_waiting)
    try:
        resp = await fetch_completion(prompt, message.text)
        ampl.track(BaseEvent(
            event_type='bot_reply',
            user_id=f'{message.from_user.id}'
        ))
    finally:
        await state.set_state(Messaging.message_inc)
    with suppress(KeyError, NameError):
        gpt_reply = resp['choices'][0]['message']['content']
        await db.save_reply(gpt_reply, conv_id)
        await message.answer(gpt_reply)
        return ampl.track(BaseEvent(
            event_type='reply_delivered',
            user_id=f'{message.from_user.id}'
        ))
    await message.answer('Sorry, can`t answer you with anything')


@router.message(Messaging.message_waiting)
async def flood_answer(message: types.Message):
    await message.answer('Please, wait for previous answer!')
