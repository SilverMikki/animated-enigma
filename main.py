from email import message
from fileinput import filename
from msilib.schema import Error
from random import randint, random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile
import voice
import mysql.connector
import time
import random
import datetime
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, reply_keyboard
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

inlineButton1 = InlineKeyboardButton('💰Магазин💰', callback_data='inlineButton1')
inlineButton2 = InlineKeyboardButton('🌕Взять мелочь🌕', callback_data='inlineButton2')
inlineButton3 = InlineKeyboardButton('⛏Отправить кацапа на работу⛏', callback_data='inlineButton3')
inlineButton4 = InlineKeyboardButton('⛏Отправить на работу⛏', callback_data='inlineButton4')
inlineButton5 = InlineKeyboardButton('🏡Вернуться с работы🏡', callback_data='inlineButton5')
inlineButton6 = InlineKeyboardButton('🏡Забрать кацапа🏡', callback_data='inlineButton6')
inlineButton7 = InlineKeyboardButton('🪝Поймать кацапа🪝', callback_data='inlineButton7')
inlineButton8 = InlineKeyboardButton('💎Поддержать разработчика💎', callback_data='inlineButton8')
inlineButton9 = InlineKeyboardButton('🗯Дальнейшие идеи🗯', callback_data='inlineButton9')
inlineButton10 = InlineKeyboardButton('🦋Все команды бота🦋', callback_data='inlineButton10')

chooseButtons1 = InlineKeyboardMarkup(row_width=1).insert(inlineButton1).insert(inlineButton2).insert(inlineButton3).insert(inlineButton4).insert(inlineButton10).insert(inlineButton9).insert(inlineButton8)
chooseButtons2 = InlineKeyboardMarkup(row_width=1).insert(inlineButton1).insert(inlineButton2).insert(inlineButton3).insert(inlineButton5).insert(inlineButton10).insert(inlineButton9).insert(inlineButton8)
chooseButtons3 = InlineKeyboardMarkup(row_width=1).insert(inlineButton1).insert(inlineButton2).insert(inlineButton4).insert(inlineButton6).insert(inlineButton10).insert(inlineButton9).insert(inlineButton8)
chooseButtons4 = InlineKeyboardMarkup(row_width=1).insert(inlineButton1).insert(inlineButton2).insert(inlineButton5).insert(inlineButton6).insert(inlineButton10).insert(inlineButton9).insert(inlineButton8)
chooseButtons5 = InlineKeyboardMarkup(row_width=1).insert(inlineButton1).insert(inlineButton2).insert(inlineButton4).insert(inlineButton7).insert(inlineButton10).insert(inlineButton9).insert(inlineButton8)
chooseButtons6 = InlineKeyboardMarkup(row_width=1).insert(inlineButton1).insert(inlineButton2).insert(inlineButton5).insert(inlineButton7).insert(inlineButton10).insert(inlineButton9).insert(inlineButton8)

voice_lib = [
InputFile("C:\\Users\\choco\\Downloads\\parsing\\voice\\warcarft3\\1.ogg"), 
InputFile("C:\\Users\\choco\\Downloads\\parsing\\voice\\warcarft3\\2.ogg"),
InputFile("C:\\Users\\choco\\Downloads\\parsing\\voice\\warcarft3\\3.ogg"),
]

text_lib = [ 
'Опять работа?!', 'Прощайте.', 'Вам меня не жалко?', 'Придется драться.', 'Ну вот, меня убьют.', 'Ты что ли король? А я за тебя не голосовал.',
'Тебя бы так!', 'Помогите! На меня давят!', 'Работа не волк, в лес не убежит.', 'Мы поймали ведьму, можно мы её сожжём?', 'Меня только что пнула лошадь. Это больно.',
'Мой молот укрепит вашу веру',
]

timer = 120

lvl = {
'0': '10',
'1': '20',
'2': '30',
'3': '40',
'4': '50',
'5': '60',
'6': '70',
'7': '80',
'8': '90',
'9': '100'
}

lvl_work = {
'0': '400',
'1': '900',
'2': '1400',
'3': '2100',
'4': '2800',
'5': '3600',
'6': '4500',
'7': '5400',
'8': '6500',
'9': '7600',
'10': '8700',
}

lvl_kazap_work = {
'0': '500',
'1': '1500',
'2': '3000',
}

lvl_kazap = {
'0': '100',
'1': '300',
'2': '700',
}

bot = Bot("1855074508:AAEFuvZkVIgZy0SB18dXRe2JK2xBV66O2eQ")
dp = Dispatcher(bot)



try:
    mydb = mysql.connector.connect(host='localhost',
                             user='root',
                             password='xxvf2pwj',
                             database='telegram',
                             )
except Exception as e:
    print(e)

def get_time(user_id):
    try:
        mycursor = mydb.cursor()
        sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `hat` FROM `users` WHERE `user_id` = %s)'
        mycursor.execute(sql, (int(user_id),))
        hat = mycursor.fetchall()
        sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `shirt` FROM `users` WHERE `user_id` = %s)'
        mycursor.execute(sql, (int(user_id),))
        shirt = mycursor.fetchall()
        sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `pants` FROM `users` WHERE `user_id` = %s)'
        mycursor.execute(sql, (int(user_id),))
        pants = mycursor.fetchall()
        sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `shoes` FROM `users` WHERE `user_id` = %s)'
        mycursor.execute(sql, (int(user_id),))
        shoes = mycursor.fetchall()
        sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `accessory` FROM `users` WHERE `user_id` = %s)'
        mycursor.execute(sql, (int(user_id),))
        accessory = mycursor.fetchall()
        return (int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))
    except Exception as e:
        print(e)

async def check_work_lvl(callback_query):
    mycursor = mydb.cursor()
    sql = 'SELECT `work_exp`, `work_lvl` FROM `users` WHERE `user_id` = %s'
    mycursor.execute(sql, (int(callback_query.from_user.id),))
    result = mycursor.fetchall()
    if(int(result[0][0]) > int(lvl_work[str(result[0][1])])):
        mycursor = mydb.cursor()
        sql = 'UPDATE `users` set `work_exp` = 0, `work_lvl` = %s where `user_id` = %s'
        mycursor.execute(sql, (int(result[0][1]) + 1, int(callback_query.from_user.id)))
        mydb.commit()
        lvl = int(result[0][1]) + 1
        message_for_delete = await bot.send_message(callback_query.message.chat.id, '🎉🎉🎉ты получил ' + str(lvl) + ' уровень работы!🎉🎉🎉')
        await asyncio.sleep(timer)
        await message_for_delete.delete()

async def check_work_lvl_kazap(callback_query):
    mycursor = mydb.cursor()
    sql = 'SELECT `kazap_work_exp`, `kazap_work_lvl` FROM `kazap` WHERE `user_id` = %s'
    mycursor.execute(sql, (int(callback_query.from_user.id),))
    result = mycursor.fetchall()
    if(int(result[0][0]) > int(lvl_kazap_work[str(result[0][1])])):
        mycursor = mydb.cursor()
        sql = 'UPDATE `kazap` set `kazap_work_exp` = 0, `kazap_work_lvl` = %s where `user_id` = %s'
        mycursor.execute(sql, (int(result[0][1]) + 1, int(callback_query.from_user.id)))
        mydb.commit()
        lvl = int(result[0][1]) + 1
        message_for_delete = await bot.send_message(callback_query.message.chat.id, '🎉🎉🎉кацап получил ' + str(lvl) + ' уровень!🎉🎉🎉')
        await asyncio.sleep(timer)
        await message_for_delete.delete()

async def check_level(message):
    mycursor = mydb.cursor()
    sql = 'SELECT `exp`, `level` FROM `users` WHERE `user_id` = %s'
    mycursor.execute(sql, (int(message.from_user.id),))
    result = mycursor.fetchall()
    if(int(result[0][0]) > int(lvl[str(result[0][1])])):
        mycursor = mydb.cursor()
        sql = 'UPDATE `users` set `exp` = 0, `level` = %s where `user_id` = %s'
        mycursor.execute(sql, (int(result[0][1]) + 1, int(message.from_user.id)))
        mydb.commit()
        lvl = int(result[0][1]) + 1
        message_for_delete = await bot.send_message(message.chat.id, '🎉🎉🎉ты получил ' + str(lvl) + ' уровень!🎉🎉🎉')
        await asyncio.sleep(timer)
        await message_for_delete.delete()

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("It works!")

@dp.callback_query_handler(lambda c: c.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if(callback_query.data == 'inlineButton1'):
        message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Магазин в пути, скоро он откроется!')
        await asyncio.sleep(timer)
        await message_for_delete.delete()
    if(callback_query.data == 'inlineButton100'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT * FROM `hat_person`'
            mycursor.execute(sql)
            result = mycursor.fetchall()
            sql = 'SELECT COUNT(`id`) FROM `hat_person`'
            mycursor.execute(sql)
            count = mycursor.fetchone()
            i = 0
            text = ''
            while i < int(count[0]):
                text = text + str(result[i][0]) + ') ' + str(result[i][1]) + ' ' + str(result[i][2]) + '%⌛️ - ' + str(result[i][3]) + '🪙 ' + str(result[i][4]) + '\n'
                i = i + 1
            message_for_delete = await bot.send_message(callback_query.message.chat.id, text)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton2'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `time_next` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(callback_query.from_user.id),))
            result = mycursor.fetchone()[0]
            time_old = result
            if(int(time.time()) > int(result)):
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(callback_query.from_user.id),))
                result = mycursor.fetchone()[0]
                get_id = callback_query.from_user.id
                money = randint(15, 30)
                money_get = money + int(result)
                timenow1 = int(time.time())
                timenext = timenow1 + (60 * 60)
                mycursor = mydb.cursor()
                sql = "UPDATE `users` set `coins` = %s, `time_now` = %s, `time_next` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(timenow1), int(timenext), get_id))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Вы успешно получили навар в размере ' + str(money) + '🏵')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (time_old - new_time)
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Невозможно использовать команду. Используйте её через ' + str(datetime.timedelta(seconds=duration)))
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton3'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap_time_work_next` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(callback_query.from_user.id),))
            result = mycursor.fetchone()[0]
            time_old = result
            if(int(time.time()) > int(result)):
                timenow1 = int(time.time())
                persent = get_time(int(callback_query.from_user.id))
                new_persent = persent / 100
                new_persent1 = (6 * 60 * 60) * new_persent
                new_persent2 = (6 * 60 * 60) - new_persent1
                timenext = timenow1 + new_persent2
                mycursor = mydb.cursor()
                sql = "UPDATE `kazap` set `is_work` = 1, `kazap_time_work_now` = %s, `kazap_time_work_next` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(timenow1), int(timenext), int(callback_query.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Правильно, гони туда этого блядского кацапа! Но помни, забери его через 6 часов!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (time_old - new_time)
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Кацап и так кирпичи таскает, куда ему ещё идти?')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton4'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `time_next_work` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(callback_query.from_user.id),))
            result = mycursor.fetchone()[0]
            time_old = result
            if(int(time.time()) > int(result)):
                timenow1 = int(time.time())
                timenext = timenow1 + (8 * 60 * 60)
                mycursor = mydb.cursor()
                sql = "UPDATE `users` set `is_work` = 1, `time_now_work` = %s, `time_next_work` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(timenow1), int(timenext), int(callback_query.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Опять работа? Ну ладно, возвращайся за наградой через 8 часов!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (time_old - new_time)
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Ты и так на работе! Тебе мало что-ли?')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton5'):
        try: 
            mycursor = mydb.cursor()
            sql = 'SELECT `is_work`, `time_next_work`, `rase`, `coins`, `work_exp` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(callback_query.from_user.id),))
            result = mycursor.fetchall()
            if(int(result[0][0]) == 1 and (int(time.time()) > int(result[0][1])) and int(result[0][2]) == 1):
                mycursor = mydb.cursor()
                money = randint(20, 40)
                exp = int(result[0][4]) + money
                money_get = (money + int(result[0][4])) + (money / 2)
                sql = "UPDATE `users` set `is_work` = 0, `coins` = %s, `work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(exp), int(callback_query.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Поздравляю с возвращением!🏆(+' + str(money) + '🌕 +' + str(money) + '🏵)')
                await check_work_lvl(callback_query)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(result[0][0]) == 1 and (int(time.time()) > int(result[0][1])) and int(result[0][2]) == 2):
                money = randint(20, 40)
                money_get = money + int(result[0][3])
                exp_get = int(result[0][4]) + (money * 2)
                sql = "UPDATE `users` set `is_work` = 0, `coins` = %s, `work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(exp_get), int(callback_query.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Поздравляю с возвращением!🏆(+' + str(money) + '🌕 +' + str(money * 2) + '🏵)')
                await check_work_lvl(callback_query)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(result[0][0]) == 1 and (int(time.time()) > int(result[0][1]))):
                money = randint(20, 40)
                money_get = money + int(result[0][4])
                exp_get = money
                sql = "UPDATE `users` set `is_work` = 0, `coins` = %s, `work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(exp_get), int(callback_query.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Поздравляю с возвращением!🏆(+' + str(money) + '🌕 +' + str(money) + '🏵)')
                await check_work_lvl(callback_query)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                if(int(result[0][0]) == 0):
                    message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Ты же не на работе, чтобы с неё возвращаться')
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
                else:
                    new_time = int(time.time())
                    duration = (int(result[0][1]) - new_time)
                    message_for_delete = await bot.send_message(callback_query.message.chat.id, 'А не рано ли ты собрался уходить, а? Тебе работать ещё ' + str(datetime.timedelta(seconds=duration)))
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton6'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `is_work`, `kazap_time_work_next`, `kazap_work_exp` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(callback_query.from_user.id),))
            result = mycursor.fetchall()
            if(int(result[0][0]) == 1 and (int(time.time()) > int(result[0][1]))):
                mycursor = mydb.cursor()
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(callback_query.from_user.id),))
                coins = mycursor.fetchone()[0]
                money = randint(10, 30)
                money_get = int(coins) + money
                exp_get = int(result[0][2]) + money 
                sql = "UPDATE `kazap` set `is_work` = 0, `kazap_work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp_get), int(callback_query.from_user.id)))
                mydb.commit()
                sql = "UPDATE `users` set `coins` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(callback_query.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'А кацап не лох!🏆(+' + str(money) + '🌕 +' + str(money) + '🏵)')
                await check_work_lvl_kazap(callback_query)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
                
            else:
                new_time = int(time.time())
                duration = (int(result[0][1]) - new_time)
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Кацап ещё ебашит, а ты жри шашлык! Ему работать ещё ' + str(datetime.timedelta(seconds=duration)))
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton7'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(callback_query.from_user.id),))
            result = mycursor.fetchone()[0]
            if(result == 0):
                mycursor = mydb.cursor()
                sql = 'SELECT `time_next_kazap` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(callback_query.from_user.id),))
                result = mycursor.fetchone()[0]
                time_old = result
                if(time.time() > result):
                    get_choice = random.choices([0, 1], weights=[70, 30], k=1)[0]
                    timenow1 = int(time.time())
                    timenext = timenow1 + (3 * 60 * 60)
                    mycursor = mydb.cursor()
                    sql = 'UPDATE `users` set `kazap` = %s, `time_now_kazap` = %s, `time_next_kazap` = %s where `user_id` = %s'
                    mycursor.execute(sql, (int(get_choice), int(timenow1), int(timenext), int(callback_query.from_user.id)))
                    mydb.commit()
                    if(get_choice == 1):
                        message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Поздравляю, кацап пойман!')
                        await asyncio.sleep(timer)
                        await message_for_delete.delete()
                        mycursor = mydb.cursor()
                        sql = 'INSERT INTO `kazap` (`user_id`, `chat_id`) VALUES (%s, %s)'
                        mycursor.execute(sql, (int(callback_query.from_user.id), int(callback_query.message.chat.id)))
                        result = mydb.commit()
                    else:
                        message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Увы, тебе не получилось поймать кацапика. Попробуй позже...')
                        await asyncio.sleep(timer)
                        await message_for_delete.delete()
                else:
                    new_time = int(time.time())
                    duration = (time_old - new_time)
                    message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Не спеши ты так с кацапом. Попробуй через ' + str(datetime.timedelta(seconds=duration)))
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Слыш, а не дохуя ли тебе кацапов будет? Разберись сначала с 1!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton8'):
        try:
            message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Ты всегда можешь поддержать меня копейкой и за это получить вознагражение\!\n\
За каждую гривну ты получишь 10💎\. Не забудь указать свой идентификатор\!\n\
Поддержать разработчика копейкой: `5375 4114 1117 9109`', parse_mode=types.ParseMode.MARKDOWN_V2)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton9'):
        try:
            message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Планы на обновления:\n\
1\) Сделать действия над кацапом, помимо посыла на работу\n\
2\) Добавить митинги для кацапов\n\
3\) Добавить квесты для пользователя\n\
4\) Добавить достижения\n\
5\) Более украсить текст\n\
6\) Добавить возможность пользоваться ботом в личные сообщения боту\n\
7\) Добавить магазин за алмазы\n\
8\) Добавить картинку на вывод информации с возможностью замены\n\
9\) Добавить возможность перевода валюты другому пользователю\n\
10\) Добавить банк\n\
Любые ваши идеи мне всегда интересны, так что пишите в ЛС @forgottenwish', parse_mode=types.ParseMode.MARKDOWN_V2)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(callback_query.data == 'inlineButton10'):
        try:
            message_for_delete = await bot.send_message(callback_query.message.chat.id, 'Список интерактивных команд:\n\n\
`обнять`, `отпиздить кацапа`, `свернуть`, `осудить`, `ширинка`, `нюдс`, `пысок`, `дрочить`, `молитва`, `ляжка`, `путин`, `связать`, `мародер`,\
`дети`, `заставить`, `повесить`, `уничтожить`, `продать`, `щекотать`, `взорвать`, `пожелать спокойной ночи`, `пожелать хорошего дня`,\
`покормить`, `одеть шапку`, `укрыть пледом`, `напоить чаем`, `покормить пирожками`, `уложить спать`, `помыть посуду`,\
`покормить кота`, `назвать котом`\n\n\
Попросить скинуть бота голосовую хуйню: `фраза рандом`, `глас мармока`\n\
`дай деняк` \- даёт пару копеек в карман\. Можно использовать раз в час\.\n\
`поймать кацапа` \- ты пытаешься поймать кацапа, если повезёт, тогда ты красавчик\! Можно использовать раз в 3 часа\.\n\
`отправиться на работу` \- ты топаешь на работу\. Баблишко забирай через 8 часов\.\n\
`вернуться с работы` \- ты возвращаешься с работы, карманы полные бабла, да\?\n\
`шо я такое` \- показывает информацию о том, что ты такое, очевидно же, да\?\n\
`шо с кацапом` \- показать информацию про твоего кацапика\n\
`русский корабль` \- отпраить кацапа в поляндию работать\n\
`забрать кацапа` \- забираешь кацапа с поляндии\n\
`покажи шапки` \- показывает магазин с шапками\n\
`за альянс!` \- теперь ты за альянс\!\n\
`за орду!` \- теперь ты за орду\!', parse_mode=types.ParseMode.MARKDOWN_V2)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

@dp.message_handler(commands=["buy_1"])
async def buy_1(message: types.Message):
    try:
        mycursor = mydb.cursor()
        sql = 'SELECT `work_lvl` FROM `users` WHERE `user_id` = %s'
        mycursor.execute(sql, (message.from_user.id,))
        result = mycursor.fetchone()[0]
        if(int(result) >= 2):
            mycursor = mydb.cursor()
            sql = 'SELECT `hat` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (message.from_user.id,))
            result = mycursor.fetchone()[0]
            if(int(result) != 2):
                mycursor = mydb.cursor()
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (message.from_user.id,))
                result = mycursor.fetchone()[0]
                if(int(result) > 500):
                    coins = int(result) - 500
                    mycursor = mydb.cursor()
                    sql = 'UPDATE `users` set `coins` = %s, `hat` = 2 where `user_id` = %s'
                    mycursor.execute(sql, (int(coins), message.from_user.id,))
                    mydb.commit()
                    message_for_delete = await bot.send_message(message.chat.id, 'Поздравляю с покупкой.')
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
                else:
                   message_for_delete = await bot.send_message(message.chat.id, 'Не хватает золотишка.')
                   await asyncio.sleep(timer)
                   await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(message.chat.id, 'У тебя уже есть эта шапка.')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        else:
            message_for_delete = await bot.send_message(message.chat.id, 'Уровень не велик для этой вещи у тебя.')
            await asyncio.sleep(timer)
            await message_for_delete.delete()
    except Exception as e:
        print(e)

@dp.message_handler(commands=["buy_2"])
async def buy_2(message: types.Message):
    try:
        mycursor = mydb.cursor()
        sql = 'SELECT `work_lvl` FROM `users` WHERE `user_id` = %s'
        mycursor.execute(sql, (message.from_user.id,))
        result = mycursor.fetchone()[0]
        if(int(result) >= 2):
            mycursor = mydb.cursor()
            sql = 'SELECT `hat` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (message.from_user.id,))
            result = mycursor.fetchone()[0]
            if(int(result) != 3):
                mycursor = mydb.cursor()
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (message.from_user.id,))
                result = mycursor.fetchone()[0]
                if(int(result) > 1000):
                    coins = int(result) - 1000
                    mycursor = mydb.cursor()
                    sql = 'UPDATE `users` set `coins` = %s, `hat` = 2 where `user_id` = %s'
                    mycursor.execute(sql, (int(coins), message.from_user.id,))
                    mydb.commit()
                    message_for_delete = await bot.send_message(message.chat.id, 'Поздравляю с покупкой.')
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
                else:
                   message_for_delete = await bot.send_message(message.chat.id, 'Не хватает золотишка.')
                   await asyncio.sleep(timer)
                   await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(message.chat.id, 'У тебя уже есть эта шапка.')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        else:
            message_for_delete = await bot.send_message(message.chat.id, 'Уровень не велик для этой вещи у тебя.')
            await asyncio.sleep(timer)
            await message_for_delete.delete()
    except Exception as e:
        print(e)

@dp.message_handler()
async def get_message(message: types.Message):
    text = message.text.lower()
    try:
        mycursor = mydb.cursor()
        sql = 'SELECT `user_id` FROM `users` WHERE `user_id` = %s'
        mycursor.execute(sql, (int(message.from_user.id),))
        result = mycursor.fetchall()
        if(result == int(message.from_user.id)):
            print(result)
        else:
            mycursor = mydb.cursor()
            if(message.from_user.username is not None and message.from_user.first_name is not None and message.from_user.last_name is not None):
                sql = 'INSERT INTO `users` (`user_id`, `chat_id`, `username`, `first_name`, `last_name`) VALUES (%s, %s, %s, %s, %s)'
                mycursor.execute(sql, (message.from_user.id, str(message.chat.id), str(message.from_user.username), str(message.from_user.first_name), str(message.from_user.last_name)))
                result = mydb.commit()
            if(message.from_user.username is not None and message.from_user.first_name is not None):
                sql = 'INSERT INTO `users` (`user_id`, `chat_id`, `username`, `first_name`) VALUES (%s, %s, %s, %s)'
                mycursor.execute(sql, (message.from_user.id, str(message.chat.id), str(message.from_user.username), str(message.from_user.first_name)))
                result = mydb.commit()
            if(message.from_user.username is not None):
                sql = 'INSERT INTO `users` (`user_id`, `chat_id`, `username`) VALUES (%s, %s, %s)'
                mycursor.execute(sql, (message.from_user.id, str(message.chat.id), str(message.from_user.username)))
                result = mydb.commit()
            if(message.from_user.first_name is not None):
                sql = 'INSERT INTO `users` (`user_id`, `chat_id`, `first_name`) VALUES (%s, %s, %s)'
                mycursor.execute(sql, (message.from_user.id, str(message.chat.id), str(message.from_user.first_name)))
                result = mydb.commit()

    except Exception as e:
        print(e)

    if(message.text == "привет"):
        await message.reply("И тебе привет!")

    if(message.text == 'дай свои команды'):
        try:
            message_for_delete = await bot.send_message(message.chat.id, "Список интерактивных команд: обнять, отпиздить кацапа, свернуть, осудить, ширинка, нюдс, пысок, дрочить, молитва, ляжка, путин, связать, мародер, дети, заставить, повесить, уничтожить, продать, щекотать, взорвать, пожелать спокойной ночи, пожелать хорошего дня, покормить, одеть шапку, укрыть пледом, напоить чаем, покормить пирожками, уложить спать, помыть посуду, покормить кота, назвать котом\n\
Попросить скинуть бота голосовую хуйню: фраза рандом, глас мармока\n\
дай деняк - даёт пару копеек в карман. Можно использовать раз в час.\n\
поймать кацапа - ты пытаешься поймать кацапа, если повезёт, тогда ты красавчик! Можно использовать раз в 3 часа.\n\
отправиться на работу - ты топаешь на работу. Баблишко забирай через 8 часов.\n\
вернуться с работы - ты возвращаешься с работы, карманы полные бабла, да?\n\
шо я такое - показывает информацию о том, что ты такое, очевидно же, да?\n\
шо с кацапом - показать информацию про твоего кацапика\n\
русский корабль - отпраить кацапа в поляндию работать\n\
забрать кацапа - забираешь кацапа с поляндии\n\
покажи шапки - показывает магазин с шапками\n\
за альянс! - теперь ты за альянс!\n\
за орду! - теперь ты за орду!")
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'мой кацап' or message.text == 'Мой кацап'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            money = mycursor.fetchone()[0]
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap = mycursor.fetchone()[0]
            sql = 'SELECT `is_work` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            is_work = mycursor.fetchone()[0]
            sql = 'SELECT `is_work` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            is_work_kazap = mycursor.fetchone()[0]
            sql = 'SELECT `level` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            level = mycursor.fetchone()[0]
            sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            exp = mycursor.fetchone()[0]
            sql = 'SELECT `diamonds` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            diamonds = mycursor.fetchone()[0]
            sql = 'SELECT `work_exp` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            work_exp = mycursor.fetchone()[0]
            sql = 'SELECT `work_lvl` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            work_lvl = mycursor.fetchone()[0]
            sql = 'SELECT `rase` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            rase_id = mycursor.fetchone()[0]
            rase = ''
            if(int(rase_id) == 1):
                rase = 'Орда🧟‍♂️'
            if(int(rase_id) == 2):
                rase = 'Альянс🧝‍♀️'
            if(int(rase_id) == 0):
                rase = 'Хихил🎅🏻'
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `hat` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            hat = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `shirt` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            shirt = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `pants` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            pants = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `shoes` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            shoes = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `accessory` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            accessory = mycursor.fetchall()
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap_name` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_name = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_lvl` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_level = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_exp` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_exp = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_work_lvl` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_work_lvl = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_work_exp` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_work_exp = mycursor.fetchone()[0]
            text_exp = ''
            if(int(exp) < int(int(lvl[str(level)]) * 0.1)):
                text_exp = '🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.2) and int(exp) > int(int(lvl[str(level)]) * 0.1)):
                text_exp = '🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.3) and int(exp) > int(int(lvl[str(level)]) * 0.2)):
                text_exp = '🌕🌕🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.4) and int(exp) > int(int(lvl[str(level)]) * 0.3)):
                text_exp = '🌕🌕🌕🌑🌑🌑🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.5) and int(exp) > int(int(lvl[str(level)]) * 0.4)):
                text_exp = '🌕🌕🌕🌕🌑🌑🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.5) and int(exp) > int(int(lvl[str(level)]) * 0.4)):
                text_exp = '🌕🌕🌕🌕🌕🌑🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.6) and int(exp) > int(int(lvl[str(level)]) * 0.5)):
                text_exp = '🌕🌕🌕🌕🌕🌕🌑🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.7) and int(exp) > int(int(lvl[str(level)]) * 0.6)):
                text_exp = '🌕🌕🌕🌕🌕🌕🌕🌑🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.8) and int(exp) > int(int(lvl[str(level)]) * 0.7)):
                text_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌑🌑'
            if(int(exp) < int(int(lvl[str(level)]) * 0.9) and int(exp) > int(int(lvl[str(level)]) * 0.8)):
                text_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌑'
            if(int(exp) < int(int(lvl[str(level)])) and int(exp) > int(int(lvl[str(level)]) * 0.9)):
                text_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕'

            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.1)):
                text_work_exp = '🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.2) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.1)):
                text_work_exp = '🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.3) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.2)):
                text_work_exp = '🌕🌕🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.4) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.3)):
                text_work_exp = '🌕🌕🌕🌑🌑🌑🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.5) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.4)):
                text_work_exp = '🌕🌕🌕🌕🌑🌑🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.5) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.4)):
                text_work_exp = '🌕🌕🌕🌕🌕🌑🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.6) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.5)):
                text_work_exp = '🌕🌕🌕🌕🌕🌕🌑🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.7) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.6)):
                text_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌑🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.8) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.7)):
                text_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌑🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)]) * 0.9) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.8)):
                text_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌑'
            if(int(work_exp) < int(int(lvl_work[str(work_lvl)])) and int(work_exp) > int(int(lvl_work[str(work_lvl)]) * 0.9)):
                text_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕'

            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.1)):
                text_kazap_exp = '🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.2) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.1)):
                text_kazap_exp = '🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.3) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.2)):
                text_kazap_exp = '🌕🌕🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.4) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.3)):
                text_kazap_exp = '🌕🌕🌕🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.5) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.4)):
                text_kazap_exp = '🌕🌕🌕🌕🌑🌑🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.5) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.4)):
                text_kazap_exp = '🌕🌕🌕🌕🌕🌑🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.6) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.5)):
                text_kazap_exp = '🌕🌕🌕🌕🌕🌕🌑🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.7) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.6)):
                text_kazap_exp = '🌕🌕🌕🌕🌕🌕🌕🌑🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.8) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.7)):
                text_kazap_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌑🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)]) * 0.9) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.8)):
                text_kazap_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌑'
            if(int(kazap_exp) < int(int(lvl_kazap[str(kazap_level)])) and int(kazap_exp) > int(int(lvl_kazap[str(kazap_level)]) * 0.9)):
                text_kazap_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕'

            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.1)):
                text_kazap_work_exp = '🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.2) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.1)):
                text_kazap_work_exp = '🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.3) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.2)):
                text_kazap_work_exp = '🌕🌕🌑🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.4) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.3)):
                text_kazap_work_exp = '🌕🌕🌕🌑🌑🌑🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.5) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.4)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌑🌑🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.5) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.4)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌕🌑🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.6) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.5)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌕🌕🌑🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.7) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.6)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌑🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.8) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.7)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌑🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.9) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.8)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌑'
            if(int(kazap_work_exp) < int(int(lvl_kazap_work[str(kazap_work_lvl)])) and int(kazap_work_exp) > int(int(lvl_kazap_work[str(kazap_work_lvl)]) * 0.9)):
                text_kazap_work_exp = '🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕'

            if(int(is_work) == 0 and int(kazap) == 0):
                    message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '\n\
Раса:' + str(rase) + '\n\
Идентификатор:' + str(message.from_user.id) + '\n\
🏵Гривны:' + str(money) + '\n\
💎Алмазы:' + str(diamonds) + '\n\
🏅Уровень:' + str(level) + '\n\
🌕Опыт: ' + str(exp) + '/' + lvl[str(level)] + text_exp + '\n\
⌛️Уменьшение времени: ' + str((int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))) + '\n\n\
⛏Уровень работы: ' + str(work_lvl) + '\n\
🌕Опыт работы: ' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + text_work_exp + '\n\n\
🎒Рюкзак:\n\n\
🪖Голова: ' + str(hat[0][0]) + '  +' + str(hat[0][1]) + '⌛️\n\
👚Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
👖Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
🥾Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️\n\
💨Аксессуар: ' + str(accessory[0][0]) + ' +' + str(accessory[0][1]) + '⌛️', reply_markup=chooseButtons5)
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
            if(int(is_work) == 1 and int(kazap) == 0):
                    message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '.\n\
Раса:' + str(rase) + '\n\
Идентификатор:' + str(message.from_user.id) + '\n\
🏵Гривны:' + str(money) + '\n\
💎Алмазы:' + str(diamonds) + '\n\
🏅Уровень:' + str(level) + '\n\
🌕Опыт: ' + str(exp) + '/' + lvl[str(level)] + text_exp + '\n\
⌛️Уменьшение времени: ' + str((int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))) + '\n\n\
⛏Уровень работы: ' + str(work_lvl) + '\n\
🌕Опыт работы: ' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + text_work_exp + '\n\n\
🎒Рюкзак:\n\n\
🪖Голова: ' + str(hat[0][0]) + '  +' + str(hat[0][1]) + '⌛️\n\
👚Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
👖Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
🥾Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️\n\
💨Аксессуар: ' + str(accessory[0][0]) + ' +' + str(accessory[0][1]) + '⌛️', reply_markup=chooseButtons6)
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
            if(int(is_work) == 0 and int(is_work_kazap) == 0 and int(kazap) == 1):
                message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '.\n\
Раса: ' + str(rase) + '\n\
Идентификатор: ' + str(message.from_user.id) + '\n\
🏵Гривны:' + str(money) + '\n\
💎Алмазы: ' + str(diamonds) + '\n\
🏅Уровень: ' + str(level) + '\n\
🌕Опыт: ' + str(exp) + '/' + lvl[str(level)] + text_exp + '\n\
⌛️Уменьшение времени: ' + str((int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))) + '\n\n\
⛏Уровень работы: ' + str(work_lvl) + '\n\
🌕Опыт работы: ' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + text_work_exp + '\n\n\
🎒Рюкзак:\n\n\
🪖Голова: ' + str(hat[0][0]) + '  +' + str(hat[0][1]) + '⌛️\n\
👚Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
👖Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
🥾Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️\n\
💨Аксессуар: ' + str(accessory[0][0]) + ' +' + str(accessory[0][1]) + '⌛️\n\n\
ℹ️Инфо кацапа: \n\n\
📝Имя кацапа: ' + str(kazap_name) + '\n\
🏅Уровень кацапика: ' + str(kazap_level) + '\n\
🌕Опыт кацапика: ' + str(kazap_exp) + '/' + lvl_kazap[str(kazap_level)] + text_kazap_exp + '\n\
⛏Уровень работы кацапа: ' + str(kazap_work_lvl) + '\n\
🌕Опыт работы кацапа: ' + str(kazap_work_exp) + '/' + lvl_kazap_work[str(kazap_work_lvl)] + text_kazap_work_exp, reply_markup=chooseButtons1)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(is_work) == 1 and int(is_work_kazap) == 0 and int(kazap) == 1):
                message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '.\n\
Раса:' + str(rase) + '\n\
Идентификатор:' + str(message.from_user.id) + '\n\
🏵Гривны:' + str(money) + '\n\
💎Алмазы:' + str(diamonds) + '\n\
🏅Уровень:' + str(level) + '\n\
🌕Опыт:' + str(exp) + '/' + lvl[str(level)] + text_exp + '\n\
⌛️Уменьшение времени: ' + str((int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))) + '\n\n\
⛏Уровень работы:' + str(work_lvl) + '\n\
🌕Опыт работы:' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + text_work_exp + '\n\n\
🎒Рюкзак:\n\n\
🪖Голова: ' + str(hat[0][0]) + '  +' + str(hat[0][1]) + '⌛️\n\
👚Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
👖Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
🥾Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️\n\
💨Аксессуар: ' + str(accessory[0][0]) + ' +' + str(accessory[0][1]) + '⌛️\n\n\
ℹ️Инфо кацапа: \n\n\
📝Имя кацапа:' + str(kazap_name) + '\n\
🏅Уровень кацапика:' + str(kazap_level) + '\n\
🌕Опыт кацапика:' + str(kazap_exp) + '/' + lvl_kazap[str(kazap_level)] + text_kazap_exp + '\n\
⛏Уровень работы кацапа:' + str(kazap_work_lvl) + '\n\
🌕Опыт работы кацапа:' + str(kazap_work_exp) + '/' + lvl_kazap_work[str(kazap_work_lvl)] + text_kazap_work_exp, reply_markup=chooseButtons2)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(is_work) == 0 and int(is_work_kazap) == 1 and int(kazap) == 1):
                message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '.\n\
Раса:' + str(rase) + '\n\
Идентификатор:' + str(message.from_user.id) + '\n\
🏵Гривны:' + str(money) + '\n\
💎Алмазы:' + str(diamonds) + '\n\
🏅Уровень:' + str(level) + '\n\
🌕Опыт: ' + str(exp) + '/' + lvl[str(level)] + text_exp + '\n\
⌛️Уменьшение времени: ' + str((int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))) + '\n\n\
⛏Уровень работы: ' + str(work_lvl) + '\n\
🌕Опыт работы: ' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + text_work_exp + '\n\n\
🎒Рюкзак:\n\n\
🪖Голова: ' + str(hat[0][0]) + '  +' + str(hat[0][1]) + '⌛️\n\
👚Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
👖Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
🥾Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️\n\
💨Аксессуар: ' + str(accessory[0][0]) + ' +' + str(accessory[0][1]) + '⌛️\n\n\
ℹ️Инфо кацапа: \n\n\
📝Имя кацапа: ' + str(kazap_name) + '\n\
🏅Уровень кацапика: ' + str(kazap_level) + '\n\
🌕Опыт кацапика: ' + str(kazap_exp) + '/' + lvl_kazap[str(kazap_level)] + text_kazap_exp + '\n\
⛏Уровень работы кацапа: ' + str(kazap_work_lvl) + '\n\
🌕Опыт работы кацапа: ' + str(kazap_work_exp) + '/' + lvl_kazap_work[str(kazap_work_lvl)] + text_kazap_work_exp, reply_markup=chooseButtons3)
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(is_work) == 1 and int(is_work_kazap) == 1 and int(kazap) == 1):
                message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '.\n\
Раса:' + str(rase) + '\n\
Идентификатор:' + str(message.from_user.id) + '\n\
🏵Гривны:' + str(money) + '\n\
💎Алмазы:' + str(diamonds) + '\n\
🏅Уровень:' + str(level) + '\n\
🌕Опыт: ' + str(exp) + '/' + lvl[str(level)] + text_exp + '\n\
⌛️Уменьшение времени: ' + str((int(hat[0][1]) + int(shirt[0][1]) + int(pants[0][1]) + int(shoes[0][1]) + int(accessory[0][1]))) + '\n\n\
⛏Уровень работы: ' + str(work_lvl) + '\n\
🌕Опыт работы: ' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + text_work_exp + '\n\n\
🎒Рюкзак:\n\n\
🪖Голова: ' + str(hat[0][0]) + '  +' + str(hat[0][1]) + '⌛️\n\
👚Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
👖Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
🥾Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️\n\
💨Аксессуар: ' + str(accessory[0][0]) + ' +' + str(accessory[0][1]) + '⌛️\n\n\
ℹ️Инфо кацапа: \n\n\
📝Имя кацапа: ' + str(kazap_name) + '\n\
🏅Уровень кацапика: ' + str(kazap_level) + '\n\
🌕Опыт кацапика: ' + str(kazap_exp) + '/' + lvl_kazap[str(kazap_level)] + text_kazap_exp + '\n\
⛏Уровень работы кацапа: ' + str(kazap_work_lvl) + '\n\
🌕Опыт работы кацапа: ' + str(kazap_work_exp) + '/' + lvl_kazap_work[str(kazap_work_lvl)] + text_kazap_work_exp, reply_markup=chooseButtons4)
                await asyncio.sleep(timer)
                await message_for_delete.delete()

                
        except Exception as e:
            print(e)

    if(message.text == 'за орду!' or message.text == 'За орду!'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `rase` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (message.from_user.id,))
            result = mycursor.fetchone()[0]
            if(int(result) == 0):
                mycursor = mydb.cursor()
                sql = "UPDATE `users` set `rase` = 1 where `user_id` = %s"
                mycursor.execute(sql, (message.from_user.id,))
                mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Да пребудут с тобой духи!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(message.chat.id, 'Ты ведь уже выбрал расу?')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'за альянс!' or message.text == 'За альянс!'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `rase` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (message.from_user.id,))
            result = mycursor.fetchone()[0]
            if(int(result) == 0):
                mycursor = mydb.cursor()
                sql = "UPDATE `users` set `rase` = 2 where `user_id` = %s"
                mycursor.execute(sql, (message.from_user.id,))
                mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Да пребудут с тобой духи!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(message.chat.id, 'Ты ведь уже выбрал расу?')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'покажи шапки' or message.text == 'Покажи шапки'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT * FROM `hat_person`'
            mycursor.execute(sql)
            result = mycursor.fetchall()
            sql = 'SELECT COUNT(`id`) FROM `hat_person`'
            mycursor.execute(sql)
            count = mycursor.fetchone()
            i = 0
            text = ''
            while i < int(count[0]):
                text = text + str(result[i][0]) + ') ' + str(result[i][1]) + ' ' + str(result[i][2]) + '%⌛️ - ' + str(result[i][3]) + '🪙 ' + str(result[i][4]) + '\n'
                i = i + 1
            message_for_delete = await bot.send_message(message.chat.id, text)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)
    
    if(message.text == 'покажи рубашки!' or message.text == 'Покажи рубашки!'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT * FROM `shirt_person`'
            mycursor.execute(sql)
            result = mycursor.fetchall()
            sql = 'SELECT COUNT(`id`) FROM `shirt_person`'
            mycursor.execute(sql)
            count = mycursor.fetchone()
            i = 0
            text = ''
            while i < int(count[0]):
                text = text + str(result[i][0]) + ') ' + str(result[i][1]) + ' ' + str(result[i][2]) + 'ур. ' + str(result[i][3]) + '% ' + str(result[i][5]) + '\n'
                i = i + 1
            message_for_delete = await bot.send_message(message.chat.id, text)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)
    
    if(message.text == 'покажи штаны!' or message.text == 'Покажи штаны!'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT * FROM `pants_person`'
            mycursor.execute(sql)
            result = mycursor.fetchall()
            sql = 'SELECT COUNT(`id`) FROM `pants_person`'
            mycursor.execute(sql)
            count = mycursor.fetchone()
            i = 0
            text = ''
            while i < int(count[0]):
                text = text + str(result[i][0]) + ') ' + str(result[i][1]) + ' ' + str(result[i][2]) + 'ур. ' + str(result[i][3]) + '% ' + str(result[i][5]) + '\n'
                i = i + 1
            message_for_delete = await bot.send_message(message.chat.id, text)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'покажи обувь!' or message.text == 'Покажи обувь!'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT * FROM `shoes_person`'
            mycursor.execute(sql)
            result = mycursor.fetchall()
            sql = 'SELECT COUNT(`id`) FROM `shoes_person`'
            mycursor.execute(sql)
            count = mycursor.fetchone()
            i = 0
            text = ''
            while i < int(count[0]):
                text = text + str(result[i][0]) + ') ' + str(result[i][1]) + ' ' + str(result[i][2]) + 'ур. ' + str(result[i][3]) + '% ' + str(result[i][5]) + '\n'
                i = i + 1
            message_for_delete = await bot.send_message(message.chat.id, text)
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    

    if(message.text == 'дай деняк' or message.text == 'Дай деняк'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `time_next` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            result = mycursor.fetchone()[0]
            time_old = result
            if(int(time.time()) > int(result)):
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                get_id = message.from_user.id
                money = randint(15, 30)
                money_get = money + int(result)
                timenow1 = int(time.time())
                timenext = timenow1 + (60 * 60)
                mycursor = mydb.cursor()
                sql = "UPDATE `users` set `coins` = %s, `time_now` = %s, `time_next` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(timenow1), int(timenext), get_id))
                mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Вы успешно получили навар в размере ' + str(money) + '🪙')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (time_old - new_time)
                message_for_delete = await bot.send_message(message.chat.id, 'Невозможно использовать команду. Используйте её через ' + str(datetime.timedelta(seconds=duration)))
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'русский корабль' or message.text == 'Русский корабль'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap_time_work_next` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            result = mycursor.fetchone()[0]
            time_old = result
            if(int(time.time()) > int(result)):
                timenow1 = int(time.time())
                timenext = timenow1 + (6 * 60 * 60)
                mycursor = mydb.cursor()
                sql = "UPDATE `kazap` set `is_work` = 1, `kazap_time_work_now` = %s, `kazap_time_work_next` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(timenow1), int(timenext), int(message.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Правильно, гони туда этого блядского кацапа! Но помни, забери его через 6 часов!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (time_old - new_time)
                message_for_delete = await bot.send_message(message.chat.id, 'Кацап и так кирпичи таскает, куда ему ещё идти?')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'забрать кацапа' or message.text == 'Забрать кацапа'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `is_work` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            result = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_time_work_next` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            old = mycursor.fetchone()[0]
            if(result == 1 and int(time.time()) > int(old)):
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                sql = 'SELECT `kazap_work_exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                kazap_work_exp = mycursor.fetchone()[0]
                money = randint(10, 30)
                money_get = int(result) + int(kazap_work_exp)
                sql = "UPDATE `kazap` set `is_work` = 0, `kazap_work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(message.from_user.id)))
                mydb.commit()
                sql = "UPDATE `users` set `coins` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(message.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Ого, кацап потный однако! Он тебе принёс аж ' + str(money) + '🪙')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (old - new_time)
                message_for_delete = await bot.send_message(message.chat.id, 'Кацап ещё ебашит, а ты жри шашлык! Ему работать ещё ' + str(datetime.timedelta(seconds=duration)))
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'шо с кацапом' or message.text == 'Шо с кацапом'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap_name` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_name = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_lvl` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_level = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_exp` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_exp = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_work_lvl` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_work_lvl = mycursor.fetchone()[0]
            sql = 'SELECT `kazap_work_exp` FROM `kazap` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            kazap_work_exp = mycursor.fetchone()[0]
            message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '\n\
📝Имя кацапа: ' + str(kazap_name) + '\n\
🎖Уровень кацапика: ' + str(kazap_level) + '\n\
🏵Опыт кацапика: ' + str(kazap_exp) + '/' + lvl_kazap[str(kazap_level)] + '\n\
🎖Уровень работы кацапа: ' + str(kazap_work_lvl) + '\n\
🏵Опыт работы кацапа: ' + str(kazap_work_exp) + '/' + lvl_kazap_work[str(kazap_work_lvl)])
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'пидарский кацапик' or message.text == 'Пидарский кацапик'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (message.from_user.id,) )
            kazap = mycursor.fetchone()[0]
            if(int(kazap) == 1):
                mycursor = mydb.cursor()
                sql = 'INSERT INTO `kazap` (`user_id`, `chat_id`) VALUES (%s, %s)'
                mycursor.execute(sql, (message.from_user.id, int(message.chat.id)))
                result = mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Кацап перезалит.')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(message.chat.id, 'У тебя же не было кацапа...')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'поймать кацапа' or message.text == 'Поймать кацапа'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `kazap` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            result = mycursor.fetchone()[0]
            if(result == 0):
                mycursor = mydb.cursor()
                sql = 'SELECT `time_next_kazap` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                time_old = result
                if(time.time() > result):
                    get_choice = random.choices([0, 1], weights=[70, 30], k=1)[0]
                    timenow1 = int(time.time())
                    timenext = timenow1 + (3 * 60 * 60)
                    mycursor = mydb.cursor()
                    sql = 'UPDATE `users` set `kazap` = %s, `time_now_kazap` = %s, `time_next_kazap` = %s where `user_id` = %s'
                    mycursor.execute(sql, (int(get_choice), int(timenow1), int(timenext), int(message.from_user.id)))
                    mydb.commit()
                    if(get_choice == 1):
                        message_for_delete = await bot.send_message(message.chat.id, 'Поздравляю, кацап пойман!')
                        await asyncio.sleep(timer)
                        await message_for_delete.delete()
                        mycursor = mydb.cursor()
                        sql = 'INSERT INTO `kazap` (`user_id`, `chat_id`) VALUES (%s, %s)'
                        mycursor.execute(sql, (int(message.from_user.id), int(message.chat.id)))
                        result = mydb.commit()
                    else:
                        message_for_delete = await bot.send_message(message.chat.id, 'Увы, тебе не получилось поймать кацапика. Попробуй позже...')
                        await asyncio.sleep(timer)
                        await message_for_delete.delete()
                else:
                    new_time = int(time.time())
                    duration = (time_old - new_time)
                    message_for_delete = await bot.send_message(message.chat.id, 'Не спеши ты так с кацапом. Попробуй через ' + str(datetime.timedelta(seconds=duration)))
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
            else:
                message_for_delete = await bot.send_message(message.chat.id, 'Слыш, а не дохуя ли тебе кацапов будет? Разберись сначала с 1!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'отправиться на работу' or message.text == 'Отправиться на работу'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `time_next_work` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            result = mycursor.fetchone()[0]
            time_old = result
            if(int(time.time()) > int(result)):
                timenow1 = int(time.time())
                timenext = timenow1 + (8 * 60 * 60)
                mycursor = mydb.cursor()
                sql = "UPDATE `users` set `is_work` = 1, `time_now_work` = %s, `time_next_work` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(timenow1), int(timenext), int(message.from_user.id)))
                mydb.commit()
                message_for_delete = await bot.send_message(message.chat.id, 'Опять работа? Ну ладно, возвращайся за наградой через 8 часов!')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                new_time = int(time.time())
                duration = (time_old - new_time)
                message_for_delete = await bot.send_message(message.chat.id, 'Ты и так на работе! Тебе мало что-ли?')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'шо я такое' or message.text == 'Шо я такое'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            money = mycursor.fetchone()[0]
            sql = 'SELECT `level` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            level = mycursor.fetchone()[0]
            sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            exp = mycursor.fetchone()[0]
            sql = 'SELECT `diamonds` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            diamonds = mycursor.fetchone()[0]
            sql = 'SELECT `work_exp` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            work_exp = mycursor.fetchone()[0]
            sql = 'SELECT `work_lvl` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            work_lvl = mycursor.fetchone()[0]
            sql = 'SELECT `rase` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            rase_id = mycursor.fetchone()[0]
            rase = ''
            if(rase_id == 1):
                rase = 'Орда🧟‍♂️'
            if(rase_id == 2):
                rase = 'Альянс🧝‍♀️'
            else:
                rase = 'Хихил🎅🏻'
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `hat` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            hat = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `shirt` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            shirt = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `pants` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            pants = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `shoes` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            shoes = mycursor.fetchall()
            sql = 'SELECT `name`, `buff` FROM `hat_person` WHERE `id` IN (SELECT `accessory` FROM `users` WHERE `user_id` = %s)'
            mycursor.execute(sql, (int(message.from_user.id),))
            accessory = mycursor.fetchall()
            message_for_delete = await bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '.\n\
Раса: ' + str(rase) + '\n\
Идентификатор: ' + str(message.from_user.id) + '\n\
В твоём кармане ' + str(money) + '🪙\n\
Брилиантики: ' + str(diamonds) + '💎\n\
Твой уровень: ' + str(level) + '\n\
Опыт: ' + str(exp) + '/' + lvl[str(level)] + '\n\
Уровень работы: ' + str(work_lvl) + '\n\
Опыт работы: ' + str(work_exp) + '/' + lvl_work[str(work_lvl)] + '\n\
Рюкзак:\n\
Голова: ' + str(hat[0][0]) + ' +' + str(hat[0][1]) + '⌛️\n\
Рубашка: ' + str(shirt[0][0]) + ' +' + str(shirt[0][1]) + '⌛️\n\
Штаны: ' + str(pants[0][0]) + ' +' + str(pants[0][1]) + '⌛️\n\
Обувь: ' + str(shoes[0][0]) + ' +' + str(shoes[0][1]) + '⌛️')
            await asyncio.sleep(timer)
            await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(message.text == 'вернуться с работы' or message.text == 'Вернуться с работы'):
        try:
            mycursor = mydb.cursor()
            sql = 'SELECT `is_work` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            result = mycursor.fetchone()[0]
            sql = 'SELECT `time_next_work` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            old = mycursor.fetchone()[0]
            sql = 'SELECT `rase` FROM `users` WHERE `user_id` = %s'
            mycursor.execute(sql, (int(message.from_user.id),))
            rase = mycursor.fetchone()[0]
            if(int(result) == 1 and (int(time.time()) > int(old)) and int(rase) == 1):
                mycursor = mydb.cursor()
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                money = randint(20, 40)
                money_get = (money + int(result)) + ((money + int(result)) / 2)
                sql = "UPDATE `users` set `is_work` = 0, `coins` = %s, `work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(money_get), int(message.from_user.id)))
                mydb.commit()
                check_work_lvl(message.from_user.id)
                message_for_delete = await bot.send_message(message.chat.id, 'Ого, та ты красавчик! ты приносишь с работы аж ' + str(money) + '🪙')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(result) == 1 and (int(time.time()) > int(old)) and int(rase) == 2):
                mycursor = mydb.cursor()
                sql = 'SELECT `work_exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                exp = mycursor.fetchone()[0]
                mycursor = mydb.cursor()
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                money = randint(20, 40)
                money_get = money + int(result)
                exp_get = exp + ((money + int(result)) / 2)
                sql = "UPDATE `users` set `is_work` = 0, `coins` = %s, `work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(exp_get), int(message.from_user.id)))
                mydb.commit()
                check_work_lvl(message.from_user.id)
                message_for_delete = await bot.send_message(message.chat.id, 'Ого, та ты красавчик! ты приносишь с работы аж ' + str(money) + '🪙')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            if(int(result) == 1 and (int(time.time()) > int(old))):
                sql = 'SELECT `coins` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                money = randint(20, 40)
                money_get = money + int(result)
                exp_get = money_get
                sql = "UPDATE `users` set `is_work` = 0, `coins` = %s, `work_exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(money_get), int(exp_get), int(message.from_user.id)))
                mydb.commit()
                check_work_lvl(message.from_user.id)
                message_for_delete = await bot.send_message(message.chat.id, 'Ого, та ты красавчик! ты приносишь с работы аж ' + str(money) + '🪙')
                await asyncio.sleep(timer)
                await message_for_delete.delete()
            else:
                if(int(result) == 0):
                    message_for_delete = await bot.send_message(message.chat.id, 'Ты же не на работе, чтобы с неё возвращаться')
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
                else:
                    new_time = int(time.time())
                    duration = (old - new_time)
                    message_for_delete = await bot.send_message(message.chat.id, 'А не рано ли ты собрался уходить, а? Тебе работать ещё ' + str(datetime.timedelta(seconds=duration)))
                    await asyncio.sleep(timer)
                    await message_for_delete.delete()
        except Exception as e:
            print(e)

    if(text == 'глас мармока'):
        try:
            await types.ChatActions.record_voice()
            await types.ChatActions.upload_voice()
            size = len(voice.marmok_voice)
            await bot.send_voice(message.chat.id, voice.marmok_voice[randint(0, size)])
        except Exception as e:
            await bot.send_message(message.chat.id, 'Мармок не хочет с тобой говорить. Не трогай его!😔😔😔')

    if (text == 'фраза рандом'): 
        try:
            await types.ChatActions.record_voice()
            await types.ChatActions.upload_voice()
            size = len(voice_lib)
            await bot.send_voice(message.chat.id, voice_lib[randint(0, size)])
        except Exception as e:
            await bot.send_message(message.chat.id, '😔😔😔')
    if(message.reply_to_message is not None):
        if(text == "обнять"):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " обнял " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == "отпиздить кацапа"):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " палкой пиздит кацапов с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == "поцеловать"):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " целует " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)
        
        if(text == 'свернуть'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " сворачивает в бараний рог " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)
        
        if(text == 'осудить'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " осуждает слова " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)
        
        if(text == 'ширинка'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " помогает расстегнуть ширинку " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'нюдс'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " скидывает сосок для " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'пысок'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " пиздит обосраным страпоном по пыску москаляке с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'дрочить'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " дрочит на " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'молитва'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " пиздит москальского падре Кирилла библией с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'путин'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " вышел на охоту за додиком с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'связать'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " связал " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'мародер'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " привязывает к столбу мародера с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'дети'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " жарит шашлык из русского дотера с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'заставить'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " заставляет стать на колени " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'повесить'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " повесил за шкирку " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'уничтожить'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " уничтожает кацапию с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'продать'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " продал на органы " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'щекотать'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " щекочет " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'взорвать'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " взрывает очко москалю с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)
        
        if(text == 'ляжка'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " кусьнул за ляжку " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'хуй'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " облизывает головку хуя " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'пожелать спокойной ночи'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " желает спокойной ночи " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'пожелать хорошего дня'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " пожелать хорошего дня " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'покормить'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " кормит вкусняшкой " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'одеть шапку'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " помогает одеть шапку " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'укрыть пледом'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " укрывает пледом " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'напоить чаем'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " поит чаем " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'покормить пирожками'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " кормит вкусными пирожками " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'уложить спать'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " укладывает спать " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'помыть посуду'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " помогает помыть посуду " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'покормить кота'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " кормит пушистого уебана вместе с " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

        if(text == 'назвать котом'):
            try:
                await types.ChatActions.typing()
                await message.answer("<a href=\""+ "tg://user?id=" + str(message.from_user.id) + "\">" + message.from_user.first_name + "</a>" + " назвала котейком " + "<a href=\""+ "tg://user?id=" + str(message.reply_to_message.from_user.id) + "\">" + message.reply_to_message.from_user.first_name + "</a>", parse_mode='HTML')
                mycursor = mydb.cursor()
                sql = 'SELECT `exp` FROM `users` WHERE `user_id` = %s'
                mycursor.execute(sql, (int(message.from_user.id),))
                result = mycursor.fetchone()[0]
                exp = result + random.choices([0, 1], weights=[60, 40], k=1)[0]
                sql = "UPDATE `users` set `exp` = %s where `user_id` = %s"
                mycursor.execute(sql, (int(exp), int(message.from_user.id)))
                mydb.commit()
                await check_level(message.from_user.id)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)