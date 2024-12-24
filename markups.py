from aiogram import types
import json

btn = types.KeyboardButton
inBtn = types.InlineKeyboardButton

def Main():
    buttons = [
        [btn(text = "Расписание"),btn(text = "Замены")],
        [btn(text = "Новости"), btn(text = "Основные контакты")]
    ]
    main_mark = types.ReplyKeyboardMarkup(keyboard=buttons)
    return main_mark

def Groups1():
    buttons = [
        [inBtn(text = "1 Курс", callback_data="1kurs")],
        [inBtn(text = "2 Курс", callback_data="2kurs")],
        [inBtn(text = "3 Курс", callback_data="3kurs")],
        [inBtn(text = "4 Курс", callback_data="4kurs")]
    ]
    rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return rulesMark

def Groups2(kurs):
    if kurs == "Allkurs":  
        buttons = [
        [inBtn(text = "Отправить всем", callback_data="Allkurs")]
    ]
    else:
        number = kurs[0:1]
        buttons = [
            [inBtn(text = f"{number}11 группа", callback_data=f"{number}11group")],
            [inBtn(text = f"{number}12 группа", callback_data=f"{number}12group")],
            [inBtn(text = f"{number}13 группа", callback_data=f"{number}13group")],
            [inBtn(text = f"{number}14 группа", callback_data=f"{number}14group")],
            [inBtn(text = f"{number}15 группа", callback_data=f"{number}15group")]
        ]
        if number == "4":
            rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons[1:5])
    rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return rulesMark

def Broadcast():
    buttons = [
        [inBtn(text = "1 Курс", callback_data="1kurs")],
        [inBtn(text = "2 Курс", callback_data="2kurs")],
        [inBtn(text = "3 Курс", callback_data="3kurs")],
        [inBtn(text = "4 Курс", callback_data="4kurs")],
        [inBtn(text = "Отправить всем", callback_data="Allkurs")]
    ]
    rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return rulesMark

def NewsMarkups(List):
    buttons = []
    for i in range(0, len(List)):
        txt = str(List[i][0])
        buttons.append([inBtn(text = txt.lower().capitalize(), callback_data=f"News_{i}")])
    rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return rulesMark

def Slider():
    buttons = [
        [inBtn(text = "<--", callback_data="Minus"), inBtn(text = "X", callback_data="Cancel"), inBtn(text= "-->", callback_data="Plus")]
    ]
    rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return rulesMark

def ZamenasMarks():
    buttons = []
    with open("data.json", 'r') as file:
        data = json.load(file)
    for x in data["Zamenas"]:
        buttons.append([inBtn(text = f"Замена на {x}", callback_data=f"Zamena_{x}")])
    buttons.append([inBtn(text=f"(Выйти)", callback_data="Exit")])
    
    rulesMark = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return rulesMark

def End():()