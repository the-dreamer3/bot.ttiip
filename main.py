from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
import logging
from aiogram.filters.command import Command
import asyncio
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import traceback


from Tkn import tkn, timetableDatabase_Chat as idData
import markups
import messages
import logHandler
import parseSite as pS
import dataHandler
from admins import admins

import os

bot = Bot(token = tkn)
dp = Dispatcher()

# - - - - - - - - NEW MEMBER LOG IN - - - - - - - - #

class newMember(StatesGroup):
    getGroup = State()
    getKurs = State()

@dp.message(Command('start'))
async def start(message: types.Message, state:FSMContext):
    if dataHandler.checkUser(message.chat.id):
        await message.answer(messages.hello(message.from_user.full_name, dataHandler.getKurs(message.from_user.id)), reply_markup=markups.Main(), parse_mode="Markdown")
    else:
        await message.answer(messages.hello(message.from_user.full_name, kurs="None"), reply_markup=markups.Groups1(), parse_mode="Markdown")
        await state.set_state(newMember.getKurs)

@dp.callback_query(newMember.getKurs)
async def start2(callback: types.CallbackQuery, state:FSMContext):
    text = callback.data
    await callback.message.edit_reply_markup(reply_markup=markups.Groups2(text))
    await callback.answer()
    await state.set_state(newMember.getGroup)

@dp.callback_query(newMember.getGroup)
async def start3(callback: types.CallbackQuery, state:FSMContext):
    if dataHandler.createUserData(callback.message.chat.id, callback.from_user.full_name, callback.data) == False:
        await callback.message.answer("Вы уже выбрали свою группу.")
    else:
        await callback.message.edit_text(text = "Спасибо за авторизацию в нашем боте!")
    await callback.answer()
    await state.clear()

class Send_Broadcast(StatesGroup):
    getGroup = State()
    getKurs = State()
    getText = State()

# - - - - - - - - - FUNCTIONAL FOR RASPISANIE BTN - - - - - - - - - #
class Shedule(StatesGroup):
    getGroup = State()
    getKurs = State()

async def SendShedule(chatId, kurs, caption):
    try:
        await bot.copy_message(
            chat_id=chatId,
            from_chat_id=idData,
            message_id=dataHandler.getMsgId_Shedule(kurs),
            caption=caption,
            reply_markup=markups.Groups1(),
            parse_mode="Markdown"
        )
    except Exception as E:
        tb = traceback.format_exception(E)
        for member in admins:
            await bot.send_message(chat_id=int(member), text = f'Админ *{admins[member]}!* Возникла ошибка: {E} |\n"{(str(tb).format())}"', parse_mode= "Markdown")

@dp.message(F.text == "Расписание")
async def SheduleMain(message: types.Message, state: FSMContext):
    await SendShedule(message.from_user.id, dataHandler.getKurs(message.from_user.id), caption="Расписание вашей группы, если желаете выбрать иное расписание, выберите ниже какое именно:")
    await state.set_state(Shedule.getGroup)

@dp.callback_query(Shedule.getGroup)
async def SheduleChoose(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=markups.Groups2(callback.data))
    await state.set_state(Shedule.getKurs)

@dp.callback_query(Shedule.getKurs)
async def SheduleChoosen(callback: types.CallbackQuery, state: FSMContext):
    group = callback.data.replace("group","")
    await SendShedule(callback.from_user.id, kurs=group, caption=f"*Расписание {group} группы*\nЕсли желаете выбрать иное расписание, выберите ниже какое именно:")
    await callback.message.delete()
    await state.set_state(Shedule.getGroup)

# - - - - - - - - - FUNCTIONAL FOR CONTACTS BTN - - - - - - - - - #
@dp.message(F.text == "Основные контакты")
async def Contacts(message: types.Message):
    await message.answer(text = messages.Contacts(), parse_mode="Markdown")


# - - - - - - - - - FUNCTIONAL FOR RASPISANIE BTN - - - - - - - - - #
class News(StatesGroup):
    getNews = State()
    Slider = State()

@dp.message(F.text == "Новости")
async def NewsList(message: types.Message, state: FSMContext):
    NewsDict = pS.DictionaryNews()
    await state.update_data(News = NewsDict)
    await message.answer(
        text = f"Недавние события нашего техникума.\nЧтобы стать частью этих событий обращайтесь к @Me4tatelnitca",
        reply_markup= markups.NewsMarkups(NewsDict),
        parse_mode="Markdown"
    )
    await state.set_state(News.getNews)

@dp.callback_query(News.getNews)
async def OneNews(callback: types.CallbackQuery, state: FSMContext):
    target = int(callback.data.split("_")[1])
    news = await state.get_data()
    news = news["News"]
    txt = f"<b><a href='{news[target][1]}'>{news[target][0]}</a></b>"
    await callback.message.edit_text(
        text = f"Новость {txt} к вашему вниманию:\n<i>Оценить статью полностью можно перейдя по ссылке</i>",
        reply_markup=markups.Slider(),
        parse_mode="HTML"
    )
    await state.set_state(News.Slider)
    await state.update_data(Slider = target)
    await SliderNews(callback, state)

@dp.callback_query(News.Slider)
async def SliderNews(callback: types.CallbackQuery, state: FSMContext):
    target = callback.data
    data = await state.get_data()
    news = data["News"]
    CheckPoint = data["Slider"]

    if (target == "Cancel"):
        await state.clear()
        await callback.message.delete()

    elif (target == "Plus"):
        if (len(news)<=CheckPoint+1): await callback.answer("It's over")
        else:
            txt = f"<b><a href='{news[CheckPoint-1][1]}'>{news[CheckPoint-1][0]}</a></b>"
            await callback.message.edit_text(
                text = f"Новость {txt} к вашему вниманию:\n<i>Оценить статью полностью можно перейдя по ссылке</i>",
                reply_markup=markups.Slider(),
                parse_mode="HTML"
            )
            await state.update_data(Slider = CheckPoint+1)
    elif (target == "Minus"):
        if (CheckPoint-1<0): await callback.answer("It's over")
        else:
            txt = f"<b><a href='{news[CheckPoint-1][1]}'>{news[CheckPoint-1][0]}</a></b>"
            await callback.message.edit_text(
                text = f"Новость {txt} к вашему вниманию:\n<i>Оценить статью полностью можно перейдя по ссылке</i>",
                reply_markup=markups.Slider(),
                parse_mode="HTML"
            )
            await state.update_data(Slider = CheckPoint-1)

# - - - - - - - - - FUNCTIONAL FOR ZAMENAS BTN - - - - - - - - - #
class Zamena(StatesGroup):
    getDate = State()

@dp.message(F.text == "Замены")
async def Zamenas(message: types.Message, state: FSMContext):
    await message.answer(text = "Выберите замену", reply_markup=markups.ZamenasMarks(), parse_mode="Markdown")
    await state.set_state(Zamena.getDate)
@dp.callback_query(Zamena.getDate)
async def SendZamena(callback: types.CallbackQuery, state: FSMContext):
    target = callback.data.split("_")[1]
    await callback.message.delete()
    await bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=idData,
        message_id=dataHandler.getMsgId_Zamena(callback.data),
        caption=f"Расписание на {target}",
        reply_markup=markups.ZamenasMarks()
    )
    await callback.answer()
    await state.clear()

# - - -- - - - - - - ADMINS - - -- - - -#
# - - - - - - - - SEND BROADCAST LOGIC - - - - - - - - #

@dp.message(Command('send')) # all or Group
async def SendBroadcast(message: types.Message, state:FSMContext):
    if str(message.from_user.id) in admins:
        await message.answer(text=f"Админ, *{message.from_user.full_name}*, выбери курс для которой будет произведена рассылка", reply_markup=markups.Broadcast(), parse_mode="Markdown")
        await state.set_state(Send_Broadcast.getGroup)
    else:
        await message.answer(text=f"*Вы не Администратор. Прошу вас не находить уязвимости кода.*", reply_markup=markups.Main(), parse_mode="Markdown")

@dp.callback_query(Send_Broadcast.getGroup)
async def getGroup(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="*Выберите группу для которой будет произведена рассылка*", reply_markup=markups.Groups2(callback.data), parse_mode="Markdown")
    await state.set_state(Send_Broadcast.getKurs)
    await callback.answer()

@dp.callback_query(Send_Broadcast.getKurs)
async def getText(callback: types.CallbackQuery, state: FSMContext):
    target = callback.data
    await callback.message.edit_text(text=f"_Напишите текст чтобы отправить его:_ *{target}*", parse_mode="Markdown")
    await state.update_data(target = target)
    await state.set_state(Send_Broadcast.getText)
    await callback.answer()

@dp.message(Send_Broadcast.getText)
async def sendEnd(message: types.Message,state: FSMContext):
    target = await state.get_data()
    await dataHandler.sendBroadcast(
        bot.send_message, message.text, target["target"]
    )
    await message.answer(text=f"Рассылка завершена.", parse_mode="Markdown")
    await state.clear()

# - - - - - - - - UPDATE R DATA BUTTON - - - - - - - - #
@dp.message(Command("update"))
async def Update(message: types.Message):
    if (str(message.from_user.id) in admins):
        await message.answer("Обновление базы данных.")
        await dataHandler.Update_R_data(message)
    else:
        await message.answer(text = "Вы не в числе админов, аливидерчи.")


@dp.message(F.text)
async def wait(message: types.Message):
    await message.reply("Не спамь, а то замену в субботу поставлю.")

dp.chosen_inline_result()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())