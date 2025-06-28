from pyrogram.filters import inline_keyboard
from pyrogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram import emoji


btn_info=KeyboardButton(f'{emoji.INFORMATION} info')
btn_games=KeyboardButton(f'{emoji.VIDEO_GAME} game')
btn_profile=KeyboardButton(f'{emoji.PERSON} profile')
btn_image=KeyboardButton(f'{emoji.FRAMED_PICTURE} image generator')

kb_main=ReplyKeyboardMarkup(keyboard=[
    [btn_info,btn_games,btn_profile,btn_image]
],resize_keyboard=True)


btn_rps=KeyboardButton(f'{emoji.PLAY_BUTTON} rock scissors paper')
btn_quest=KeyboardButton(f'{emoji.CITYSCAPE_AT_DUSK} quest')
btn_back=KeyboardButton(f'{emoji.BACK_ARROW} back')

kb_games=ReplyKeyboardMarkup(keyboard=[
    [btn_rps],
    [btn_quest,btn_back]
],resize_keyboard=True)


btn_rock=KeyboardButton(f'{emoji.ROCK} rock')
btn_scissors=KeyboardButton(f'{emoji.SCISSORS} scissors')
btn_paper=KeyboardButton(f'{emoji.NOTEBOOK} paper')

kb_rps=ReplyKeyboardMarkup(keyboard=[
    [btn_rock,btn_scissors,btn_paper]
],resize_keyboard=True)


inline_kb_start_quest=InlineKeyboardMarkup([
    [InlineKeyboardButton('Пройти квест',callback_data='start_quest')]
])

inline_kb_choice_door=InlineKeyboardMarkup([
    [InlineKeyboardButton('⬅🚪Левая дверь',callback_data='left_door')],
    [InlineKeyboardButton('➡🚪Правая дверь',callback_data='right_door')]
])

inline_kb_left_door=InlineKeyboardMarkup([
    [InlineKeyboardButton('🐉Сразится с драконом',callback_data='dragon')],
    [InlineKeyboardButton('🏃Сбежать',callback_data='run')]
])

inline_kb_right_door=InlineKeyboardMarkup([
    [InlineKeyboardButton('💎Алмаз',callback_data='diamond')],
    [InlineKeyboardButton('🗡Меч короля',callback_data='kings_sword')],
     [InlineKeyboardButton('📕Книга чародея',callback_data='book')]
])

