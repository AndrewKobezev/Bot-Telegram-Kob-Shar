import os
import random
from dotenv import load_dotenv
import telebot
from telebot import types

# Загрузка токена
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена. Убедитесь, что файл .env существует и содержит токен.")

bot = telebot.TeleBot(TOKEN)

# Состояния и инвентарь
user_states = {}
user_inventory = {}

STATES = {
    "start": "start",
    "choose_entry_point": "choose_entry_point",
    "office_zone": "office_zone",
    "underground": "underground",
    "roof": "roof",
    "inside_building": "inside_building",
    "server_room_choice": "server_room_choice",
    "final_corona": "final_corona",
    "end_game": "end_game"
}

ITEMS = [
    "Планшет",
    "Газовая капсула",
    "Маскировочный костюм M3",
    "Голосовой клонер",
    "Дрон-приманка",
]

def get_keyboard(options):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for option in options:
        markup.add(types.KeyboardButton(option))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = STATES["start"]
    user_inventory[user_id] = ITEMS.copy()

    welcome_text = (
        "👁️ Приветствую, Агент Ноль.\n\n"
        "Твоя миссия — устранить или обезвредить объект по имени \"Корона\". "
        "Он скрывается в административной башне \"Этернис\".\n\n"
        "У тебя есть доступ к следующим инструментам:\n"
        + "\n".join(f"- {item}" for item in user_inventory[user_id]) +
        "\n\n🔍 Выбери путь проникновения:"
    )

    keyboard = get_keyboard(["Через офисную зону", "Через подземные коммуникации", "С крыши"])
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    state = user_states.get(user_id, STATES["start"])

    if message.text == "/start":
        start(message)
        return

    if state == STATES["start"]:
        handle_entry_point(message)
    elif state == STATES["office_zone"]:
        handle_office_zone(message)
    elif state == STATES["underground"]:
        handle_underground(message)
    elif state == STATES["roof"]:
        handle_roof(message)
    elif state == STATES["inside_building"]:
        handle_inside_building(message)
    elif state == STATES["server_room_choice"]:
        handle_server_room(message)
    elif state == STATES["final_corona"]:
        handle_final_choice(message)
    else:
        bot.send_message(message.chat.id, "🤖 Я тебя не понял. Напиши /start для начала.")

def handle_entry_point(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Через офисную зону":
        user_states[user_id] = STATES["office_zone"]
        text = "🪪 На тебе маскировочный костюм. Охранник проверяет документы. Что будешь делать?"
        options = ["Вернуться обратно"]
        
        if "Планшет" in user_inventory[user_id]:
            options.append("Использовать планшет для фальшивых прав")
        if "Голосовой клонер" in user_inventory[user_id]:
            options.append("Воспользоваться голосовым клонером")
        if "Дрон-приманка" in user_inventory[user_id]:
            options.append("Отвлечь внимание дроном-приманкой")
            
        keyboard = get_keyboard(options)
        
    elif choice == "Через подземные коммуникации":
        user_states[user_id] = STATES["underground"]
        text = "🕳️ Ты находишь аварийную шахту. Решётка закрыта, но ты можешь её вскрыть. Что будешь делать?"
        options = [
            "Вскрыть решётку и проникнуть внутрь",
            "Использовать анализатор, чтобы проверить на наличие датчиков",
            "Вернуться обратно"
        ]
        if "Газовая капсула" in user_inventory[user_id]:
            options.insert(2, "Использовать газ, если там сторожевые собаки")
        keyboard = get_keyboard(options)
        
    elif choice == "С крыши":
        user_states[user_id] = STATES["roof"]
        text = "🦅 Ты на крыше. Ниже — сигнализация и ангар. Как действовать?"
        options = [
            "Проверить крышу с помощью дрона",
            "Спуститься напрямую на верёвке",
            "Вернуться обратно"
        ]
        if "Маскировочный костюм M3" in user_inventory[user_id]:
            options.insert(1, "Включить блокиратор сигнализации")
        keyboard = get_keyboard(options)
        
    else:
        bot.send_message(message.chat.id, "❌ Неизвестный маршрут.")
        return

    bot.send_message(message.chat.id, text, reply_markup=keyboard)

def handle_office_zone(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        user_states[user_id] = STATES["start"]
        start(message)
        return

    success = False
    
    if choice == "Использовать планшет для фальшивых прав":
        if "Планшет" in user_inventory[user_id]:
            user_inventory[user_id].remove("Планшет")
            bot.send_message(message.chat.id, "📱 Ты показал охраннику поддельные документы с планшета. Он пропускает тебя.")
            success = True
        else:
            bot.send_message(message.chat.id, "❌ У тебя нет планшета!")
            
    elif choice == "Воспользоваться голосовым клонером":
        if "Голосовой клонер" in user_inventory[user_id]:
            user_inventory[user_id].remove("Голосовой клонер")
            bot.send_message(message.chat.id, "🎙️ Ты скопировал голос начальника охраны и отдал приказ пропустить тебя.")
            success = True
        else:
            bot.send_message(message.chat.id, "❌ У тебя нет голосового клонера!")
            
    elif choice == "Отвлечь внимание дроном-приманкой":
        if "Дрон-приманка" in user_inventory[user_id]:
            user_inventory[user_id].remove("Дрон-приманка")
            bot.send_message(message.chat.id, "🛸 Дрон отвлёк охрану, и ты смог проскользнуть незамеченным.")
            success = True
        else:
            bot.send_message(message.chat.id, "❌ У тебя нет дрона-приманки!")
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

    if success:
        bot.send_message(message.chat.id, "✅ Ты успешно проник в здание!")
        user_states[user_id] = STATES["inside_building"]
        send_inside_building_options(message)

def handle_underground(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        user_states[user_id] = STATES["start"]
        start(message)
        return

    success = False
    
    if choice == "Вскрыть решётку и проникнуть внутрь":
        if random.random() > 0.3:  # 70% шанс успеха
            bot.send_message(message.chat.id, "🔧 Ты тихо вскрыл решётку и проник внутрь.")
            success = True
        else:
            bot.send_message(message.chat.id, "⚠️ Ты задел сигнализацию! Пришлось отступить.")
            
    elif choice == "Использовать анализатор, чтобы проверить на наличие датчиков":
        bot.send_message(message.chat.id, "📡 Анализатор показал безопасный путь. Ты проник внутрь.")
        success = True
        
    elif choice == "Использовать газ, если там сторожевые собаки":
        if "Газовая капсула" in user_inventory[user_id]:
            user_inventory[user_id].remove("Газовая капсула")
            bot.send_message(message.chat.id, "💨 Ты выпустил усыпляющий газ и нейтрализовал собак.")
            success = True
        else:
            bot.send_message(message.chat.id, "❌ У тебя нет газовой капсулы!")
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

    if success:
        bot.send_message(message.chat.id, "✅ Ты теперь внутри здания.")
        user_states[user_id] = STATES["inside_building"]
        send_inside_building_options(message)

def handle_roof(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        user_states[user_id] = STATES["start"]
        start(message)
        return

    success = False
    
    if choice == "Проверить крышу с помощью дрона":
        if "Дрон-приманка" in user_inventory[user_id]:
            user_inventory[user_id].remove("Дрон-приманка")
            bot.send_message(message.chat.id, "🛸 Дрон показал безопасный путь для спуска.")
            success = True
        else:
            bot.send_message(message.chat.id, "❌ У тебя нет дрона-приманки!")
            
    elif choice == "Включить блокиратор сигнализации":
        if "Маскировочный костюм M3" in user_inventory[user_id]:
            bot.send_message(message.chat.id, "📶 Блокиратор сигнализации активирован. Ты безопасно спустился.")
            success = True
        else:
            bot.send_message(message.chat.id, "❌ Твой костюм не поддерживает эту функцию!")
            
    elif choice == "Спуститься напрямую на верёвке":
        if random.random() > 0.5:  # 50% шанс успеха
            bot.send_message(message.chat.id, "🧗 Ты успешно спустился, избежав детекторов движения.")
            success = True
        else:
            bot.send_message(message.chat.id, "⚠️ Ты задел лазерный луч! Пришлось вернуться на крышу.")
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

    if success:
        bot.send_message(message.chat.id, "🏢 Ты теперь внутри здания.")
        user_states[user_id] = STATES["inside_building"]
        send_inside_building_options(message)

def send_inside_building_options(message):
    user_id = message.from_user.id
    options = [
        "Найти секретаря и получить информацию о графике Короны",
        "Проникнуть в серверную комнату",
        "Перейти к финальному этажу напрямую"
    ]
    if "Планшет" in user_inventory[user_id]:
        options.insert(0, "Изучить данные на планшете")
    keyboard = get_keyboard(options)
    bot.send_message(message.chat.id, "Выбери дальнейшее действие:", reply_markup=keyboard)

def handle_inside_building(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Изучить данные на планшете":
        if "Планшет" in user_inventory[user_id]:
            bot.send_message(message.chat.id, 
                "📊 На планшете маршрут Короны и слабые места в охране:\n"
                "- Корона будет один в своём кабинете с 14:00 до 15:00\n"
                "- Охрана меняется каждые 2 часа\n"
                "- Есть слепые зоны в системе наблюдения")
        else:
            bot.send_message(message.chat.id, "❌ У тебя нет планшета!")
            
    elif choice == "Найти секретаря и получить информацию о графике Короны":
        bot.send_message(message.chat.id, 
            "📄 Секретарь рассказал:\n"
            "- Корона сегодня задержится до 18:00\n"
            "- В 15:30 у него совещание\n"
            "- Кабинет на 25 этаже")
            
    elif choice == "Проникнуть в серверную комнату":
        user_states[user_id] = STATES["server_room_choice"]
        bot.send_message(message.chat.id, 
            "🔒 Ты подошёл к серверной комнате. На двери кодовый замок. Что будешь делать?",
            reply_markup=get_keyboard([
                "Попробовать взломать замок",
                "Искать обходные пути",
                "Вернуться к выбору действий"
            ]))
            
    elif choice == "Перейти к финальному этажу напрямую":
        handle_final_dialog(message)
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

def handle_server_room(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться к выбору действий":
        user_states[user_id] = STATES["inside_building"]
        send_inside_building_options(message)
        return
        
    if choice == "Попробовать взломать замок":
        if random.random() > 0.4:  # 60% шанс успеха
            bot.send_message(message.chat.id, 
                "💻 Ты успешно взломал систему!\n"
                "Серверные данные показали:\n"
                "- Корона - искусственный интеллект\n"
                "- Он контролирует всю систему безопасности")
            handle_final_dialog(message)
        else:
            bot.send_message(message.chat.id, 
                "⚠️ Взлом не удался! Сработала сигнализация.\n"
                "Придётся действовать быстрее.")
            handle_final_dialog(message)
            
    elif choice == "Искать обходные пути":
        bot.send_message(message.chat.id, 
            "🚪 Ты нашёл технический вход через вентиляцию.\n"
            "Внутри обнаружил документы:\n"
            "- План эвакуации Короны\n"
            "- Карта всех камер наблюдения")
        handle_final_dialog(message)
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

def handle_final_dialog(message):
    user_id = message.from_user.id
    user_states[user_id] = STATES["final_corona"]

    bot.send_message(message.chat.id,
        "👤 Ты встретил Корону. Он говорит:\n\n"
        "«Я не враг. Я внедрённый агент. Мои данные спасут страну. "
        "Ты готов мне поверить?»\n\n"
        "Ты замечаешь, что он держит руку близко к тревожной кнопке...",
        reply_markup=get_keyboard([
            "Устранить его немедленно",
            "Выслушать его",
            "Забрать его с собой",
            "Оставить его в покое"
        ])
    )

def handle_final_choice(message):
    user_id = message.from_user.id
    choice = message.text

    endings = {
        "Устранить его немедленно": (
            "💀 Ты выстрелил первым. Корона падает, но успевает нажать кнопку.\n"
            "Сирены! Ты выполнил миссию, но теперь ты - следующая цель.\n\n"
            "🔚 Конец: Жестокая необходимость"
        ),
        "Выслушать его": (
            "⚖️ Ты решаешь выслушать его. Он передаёт тебе флешку с данными.\n"
            "«Это доказательства предательства в верхушке агентства»\n\n"
            "🔚 Конец: Неожиданный союзник"
        ),
        "Забрать его с собой": (
            "✅ «Хорошо, но мы уходим сейчас!» - говоришь ты.\n"
            "Вы покидаете здание до срабатывания тревоги.\n"
            "Позже данные Короны помогают раскрыть заговор.\n\n"
            "🔚 Конец: Идеальное завершение"
        ),
        "Оставить его в покое": (
            "🔍 «Я проверю твою историю» - говоришь ты, уходя.\n"
            "Ты начинаешь собственное расследование, но Корона исчезает.\n\n"
            "🔚 Конец: Незавершённое дело"
        )
    }

    result = endings.get(choice)
    if result:
        bot.send_message(message.chat.id, result)
        bot.send_message(message.chat.id, 
            "Спасибо за прохождение! Напиши /start, чтобы начать заново.",
            reply_markup=types.ReplyKeyboardRemove())
        user_states[user_id] = STATES["end_game"]
    else:
        bot.send_message(message.chat.id, "❌ Неизвестный выбор. Попробуй снова.")

# Запуск
bot.polling(none_stop=True)
