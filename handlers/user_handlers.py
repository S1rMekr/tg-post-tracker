from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_track_info_list, create_track_and_get_id, get_last_track_info
from database.database import users_db


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=None)
    

@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=None)


@router.message(F.text == 'Добавить трек')
async def process_add_track_command(message: Message):
    await message.answer(text=LEXICON_RU['add_track'], reply_markup=None)
    

@router.message(Command(commands="track"))
async def process_track_command(message: Message):
    track_info = get_track_info_list(users_db[message.from_user.id])
    await message.answer(text=track_info, reply_markup=None)

@router.message(Command(commands="last"))
async def process_last_command(message: Message):
    track_info = get_last_track_info(users_db[message.from_user.id])
    await message.answer(text=track_info, reply_markup=None)

@router.message()
async def process_get_track_id_command(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = create_track_and_get_id(message.text)
    await message.answer(text=LEXICON_RU['track_success'], reply_markup=None)