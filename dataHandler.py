import os
import json
from datetime import datetime
import asyncio
import traceback
import admins
from aiogram import Bot, Dispatcher, types
from Tkn import tkn, timetableDatabase_Chat as id_Data

class KursNotFound_Exeption(Exception):
     def __init__(self, message):
        self.message = message

pathToBase = "data.json"
bot = Bot(token = tkn)

async def Update_R_data(message: types.Message):
    count = 0
    errorChecker = 0
    with open(pathToBase, "r", encoding="utf-8") as file:
        dataRead = json.load(file)
        dataRead["Shedule"] = {}
        dataRead["Zamenas"] = {}
        btns = []
        for x in range(0,100):
            try:
                a = await bot.forward_message(chat_id=message.from_user.id, from_chat_id=id_Data, message_id=x)
                capture = a.caption
                if capture.__contains__("Shedule"):
                    group = capture.replace("Shedule_", "")
                    count+=1
                    await message.answer(text = f"{capture}")
                    
                    dataRead["Shedule"][group] = x
                
                elif capture.__contains__("Zamena_"):
                    zamena = capture.replace("Zamena_", "")
                    count+=1
                    await message.answer(text = f"{capture}")
                    # btns.append(f'    [inBtn(text = "Замены на {zamena}", callback_data="Zamena_{zamena}")]')
                   
                    dataRead["Zamenas"][str(zamena)] = x

                await bot.delete_message(chat_id=message.from_user.id, message_id=a.message_id)
            except:
                if(count>0):errorChecker+=1
            if errorChecker>10: break

        await message.answer(text = f"Total message update: {count}")
    
    file.close()
    with open(pathToBase, 'w',  encoding='utf-8') as file:
        json.dump(dataRead, file, indent=4)    

def getMsgId_Shedule(course):
    with open(pathToBase, 'r') as file:
        data = json.load(file)
    course = course.replace("group", "")
    temp = data["Shedule"][course]
    file.close()
    return temp 

def getMsgId_Zamena(datetime):
    datetime = datetime.split("_")[1].split(" ")[0]
    with open(pathToBase, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for x in data["Zamenas"]:
            if str(x).__contains__(datetime):
                file.close()
                return data["Zamenas"][x]
    file.close()

def getKurs(id):
    with open(pathToBase, 'r') as file:
        data = json.load(file)
        for x in data["Groups"]:
            if str(data["Groups"][x]).__contains__(str(f"{id}")):
                return x
        raise KursNotFound_Exeption()

def createUserData(chatId, userName, group):
    with open(pathToBase, 'r') as file:
        if file.read().__contains__(str(chatId)): file.close(); return False
        # file.close()
    group = group.replace("group", "")
    with open(pathToBase, 'r') as file:
        data = json.load(file)

        if group not in data:
            data["Groups"][group] = {}
        if "users" not in data["Groups"][group]:
            data["Groups"][group]["users"] = {}

        if chatId not in data["Groups"][group]["users"]:
            data["Groups"][group]["users"][chatId] = {}

        data["Groups"][group]["users"][chatId] = {
                    "userName": userName
                }
        file.close()
    
    with open(pathToBase, 'w') as file:
        json.dump(data, file, indent=4)
        file.close()

def checkUser(chatId):
    with open(pathToBase, 'r') as file:
        if file.read().__contains__(str(chatId)): file.close(); return True        

async def sendBroadcast(sendFunction, text, group = None):
    with open(pathToBase, 'r') as file:
        data = json.load(file)
        if group.__contains__("All"):
            for group in data["Groups"]:
                try:
                    for chatId in data["Groups"][group]["users"]:
                        text = text
                        await sendFunction(int(chatId), text, parse_mode = "Markdown")
                except: ()
        elif group.__contains__("group"):
            group = group.replace("group", "")
            try:
                for member in data["Groups"][group]["users"]:
                        chatId = member
                        text = text
                        await sendFunction(int(chatId), text, parse_mode = "Markdown")
            except Exception as E:
                tb = traceback.format_exception(E)
                for member in admins.admins:
                    await sendFunction(member, f'Админ *{admins[member]}!* Возникла ошибка: {E} |\n"{(str(tb).format())}"', parse_mode= "Markdown")

