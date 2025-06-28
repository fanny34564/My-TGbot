import random

import json


from pyrogram import Client,filters
from pyrogram.filters import reply
from gen import generate
import base64

import config
import keyboards
from pyrogram.types import ForceReply

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="Витя Пьянуковичь",  # можно указать любое имя
)

def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text
    return filters.create(func, "ButtonFilter", button=button)


@bot.on_message(filters.command('about')|button_filter(keyboards.btn_info))
async def about(bot,message):
    await message.reply(f'Мое имя {message.from_user.first_name} и мне 12 лет')

@bot.on_message(filters.command('start'))
async def start(bot,message):
    await message.reply(f'Привет {message.from_user.first_name} я твой бот!',reply_markup=keyboards.kb_main)
    with open('users.json','r') as file:
        users=json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id]={'score':100, 'name':message.from_user.first_name}
        with open('users.json','w') as file:
            json.dump(users,file,indent=4,ensure_ascii=False)

@bot.on_message(filters.command('sticker'))
async def sticker(bot,message):
    await bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAENByNnH7E3x_hT00RHkBA5kiCtYTf4aAAC2hQAAp6QGVCfJrPWVxowoTYE')

@bot.on_message(filters.command('picture')|button_filter(keyboards.btn_profile))
async def picture(bot,message):
    await bot.send_photo(message.chat.id,'https://i.ytimg.com/vi/ALfsBUKBBkg/maxresdefault.jpg')
    await bot.send_document(message.chat.id,'https://steamuserimages-a.akamaihd.net/ugc/809998067557208548/2A483A94C68E6DD89A5C36ECA6465E927CAA780F/?imw=512&amp;imh=372&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true')

@bot.on_message(filters.command('games')|button_filter(keyboards.btn_games))
async def games(bot,message):
    await message.reply('Выбери игру',reply_markup=keyboards.kb_games)

@bot.on_message(filters.command('back')|button_filter(keyboards.btn_back))
async def back(bot,message):
    await message.reply('Главное меню',reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('game')|button_filter(keyboards.btn_rps))
async def game(bot,message):
    with open('users.json','r') as file:
        users=json.load(file)
    if users[str(message.from_user.id)]['score']>=10:
        await message.reply('Сделай свой ход',reply_markup=keyboards.kb_rps)
    else:
        await message.reply('Не хватает средств')

@bot.on_message(button_filter(keyboards.btn_rock)|button_filter(keyboards.btn_scissors)|button_filter(keyboards.btn_paper))
async def rps(bot,message):
    with open('users.json','r') as file:
        users=json.load(file)
    rock=keyboards.btn_rock.text
    scissors=keyboards.btn_scissors.text
    paper=keyboards.btn_paper.text
    pc=random.choice([rock,scissors,paper])
    user=message.text
    if user==pc:
        await message.reply('Ничья')
    elif (user == rock and pc == scissors) or (user == scissors and pc == paper) or (user == paper and pc == rock):
        await message.reply('Вы выйграли!')
        users[str(message.from_user.id)]['score'] +=10
    else:
        await message.reply('Вы проиграли!')
        users[str(message.from_user.id)]['score'] -=10
    with open('users.json','w') as file:
        json.dump(users,file,indent=4,ensure_ascii=False)

@bot.on_message(button_filter(keyboards.btn_quest))
async def quest(bot,message):
    await message.reply_text('Хотите пройти квест?',reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def start_quest(bot,query):
    if query.data=='start_quest':
        await query.answer(text='Вы попали в квест!',show_alert=True)
        await query.message.reply_text('Перед вами две двери, какую выберите',reply_markup=keyboards.inline_kb_choice_door)
        await query.message.delete()
    if query.data == 'left_door':
        await query.answer(text='Перед вами дракон!', show_alert=True)
        await query.message.reply_text('Будете сражаться или убежите',reply_markup=keyboards.inline_kb_left_door)
        await query.message.delete()
    if query.data == 'right_door':
        await query.answer(text='Сокровища!', show_alert=True)
        await query.message.reply_text('Какое выберите',reply_markup=keyboards.inline_kb_right_door)
        await query.message.delete()
    if query.data == 'dragon':
        await query.answer(text='Вы попытались сразиться с драконом и погибли!', show_alert=True)
        await query.message.delete()
    if query.data == 'run':
        await query.answer(text='Вы убежали и остались в живых!', show_alert=True)
        await query.message.delete()
    if query.data == 'diamond':
        await query.answer(text='Вы подобрали алмаз и стали самым богатым человеком!', show_alert=True)
        await query.message.delete()
    if query.data == 'kings_sword':
        await query.answer(text='Вы взяли меч короля и стали самым сильным!', show_alert=True)
        await query.message.delete()
    if query.data == 'book':
        await query.answer(text='Вы подобрали книгу и стали великим магом!', show_alert=True)
        await query.message.delete()

@bot.on_message(filters.command("image"))
async def image(bot,message):
    if len(message.text.split()) > 1:
        query=message.text.replace('/image','')
        await message.reply_text(f'Генерирую изображение по запросу {query}, подождите...')
        images=await  generate(query)
        if images:
            image_data=base64.b64decode(images[0])
            with open('image.png','wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id,'image.png',reply_to_message_id=message.id)
        else:
            await message.reply_text('Что-то пошло не так')
    else:
        await message.reply_text('Вы не ввели запрос')

query_text='Введите запрос для генерации изображения'
@bot.on_message(button_filter(keyboards.btn_image))
async def image_commnd(bot,message):
    await message.reply(query_text, reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def image_reply(bot,message):
    if message.reply_to_message.text==query_text:
        query=message.text
        await message.reply_text(f'Генерирую изображение по запросу {query}, подождите...')
        images = await  generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            with open('image.png', 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, 'image.png', reply_to_message_id=message.id)
        else:
            await message.reply_text('Что-то пошло не так',
            reply_to_message_id=message.id,
            reply_markup=keyboards.kb_main)














@bot.on_message()
async def eho(bot,message):
    await message.reply(f'{message.from_user.first_name} прислал: {message.text}')


bot.run()