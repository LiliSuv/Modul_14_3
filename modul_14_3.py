from aiogram import Bot, Dispatcher, executor, types
from aiogram. contrib. fsm_storage. memory import MemoryStorage
from aiogram. dispatcher. filters. state import State, StatesGroup
from aiogram. dispatcher import FSMContext
from aiogram. types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from aiogram. types import InlineKeyboardMarkup, InlineKeyboardButton
import prige_list

api = '8..........C6yc'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button, button2)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3=KeyboardButton(text="Купить")
kb1.row(button, button2,button3)

kb2=InlineKeyboardMarkup()
b = InlineKeyboardButton(text='Product1', callback_data="product_buying1")
b1 = InlineKeyboardButton(text='Product2', callback_data="product_buying2")
b2 = InlineKeyboardButton(text='Product3', callback_data="product_buying3")
b3 = InlineKeyboardButton(text='Product4', callback_data="product_buying4")
kb2.row( b,b1, b2,b3)


kb3=InlineKeyboardMarkup()
button=InlineKeyboardButton(text="Купить!",callback_data="product_bu")
button1=InlineKeyboardButton(text="Назад", callback_data='back_to_catalog')
kb3.row( button,button1)


class UserState(StatesGroup):
    age=State()
    growth=State()
    weight= State()


@dp.message_handler (text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию',reply_markup = kb)


@dp.message_handler (text='Информация')
async def inform(message):
    await message. answer ( 'Я бот, помогающий твоему здоровью')


@dp.message_handler (text='Купить')
async def get_buying_list(message):
    await message. answer ( 'Продукция',reply_markup = kb2)


@dp.callback_query_handler(text = "product_buying1")
async def product_1(call):
    with open ('files/1.png', 'rb') as img:
        await call.message.answer_photo (img,prige_list.Product1,reply_markup=kb3)
        await call. answer()


@dp.callback_query_handler(text = "product_buying2")
async def product_2(call):
    with open ('files/2.png', 'rb') as img:
        await call.message.answer_photo (img, prige_list.Product2, reply_markup=kb3)
        await call.answer ()


@dp.callback_query_handler(text = "product_buying3")
async def product_3(call):
    with open ('files/3.png', 'rb') as img:
        await call.message.answer_photo (img, prige_list.Product3, reply_markup=kb3)
        await call.answer ()


@dp.callback_query_handler(text = "product_buying4")
async def product_4(call):
    with open ('files/4.png', 'rb') as img:
        await call.message.answer_photo (img, prige_list.Product4, reply_markup=kb3)
        await call.answer ()



@dp.callback_query_handler(text = "product_bu")
async def product_bu(call):
    await call. message. answer ('Вы успешно приобрели продукт. Спасибо за покупку.')
    await call. answer()


@dp.callback_query_handler(text = "back_to_catalog")
async def back_to_catalog(call):
    await call. message. answer ('Вам не понравилось наше предложение? Обидно! Попробуйте еще раз ознакомиться с нашей продукцией.')
    await call.message.answer ('Продукция', reply_markup=kb2)
    await call. answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.answer ("Введите свой возраст")
    await UserState.age.set ()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer ("Привет!  Что Вас интересует?",reply_markup = kb1)


@dp.message_handler()
async def all_message(message):
    await message.answer ("Введите команду /start, чтобы начать общение")


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer ('Введите свой рост:')
    await UserState.growth.set ()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data (growth=message.text)
    await message.answer ('Введите свой вес:')
    await UserState.weight.set ()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data (weight=message.text)
    data=await state.get_data ()
    try:
        int(data['weight'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой вес')
        await state.finish ()
    else:
        if int (data['weight']) > 0 and int (data['weight']) < 350:
            int (data['weight'])
        else:
            data['weight'] = 'fff'
            await message.answer ('Вы не правильно ввели свой вес')
            await state.finish ()
    try:
        int(data['age'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой возраст')
        await state.finish ()
    else:
        if  int(data['age']) > 0 and  int(data['age']) < 120:
            int(data['age'])
        else:
            data['age'] = 'fff'
            await message.answer ('Вы не правильно ввели свой возраст')
            await state.finish ()
    try:
        int(data['growth'])
    except Exception:
        await message.answer ('Вы не правильно ввели свой рост')
        await state.finish ()
    else:
        if  int(data['growth']) > 50 and  int(data['growth']) < 210:
            int(data['growth'])
        else:
            data['growth'] = 'fff'
            await message.answer ('Вы не правильно ввели свой рост')
            await state.finish ()


    a=10*int(data['weight'])+6.25 * int(data['growth'])-5*int(data['age'])-161
    await message.answer(f'Ваша норма каллорий {a}')
    await state.finish ()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула расчета калорий для женщины:\n 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

