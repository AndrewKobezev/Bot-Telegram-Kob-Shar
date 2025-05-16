import os
from dotenv import load_dotenv
import telebot
from telebot import types

# Загрузка токена
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена. Убедись, что файл .env существует и содержит токен.")

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
        "- Планшет\n- Газовая капсула\n- Маскировочный костюм M3\n"
        "- Голосовой клонер\n- Дрон-приманка\n\n"
        "🔍 Выбери путь проникновения:"
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
        keyboard = get_keyboard([
            "Использовать планшет для фальшивых прав",
            "Воспользоваться голосовым клонером",
            "Отвлечь внимание дроном-приманкой",
            "Вернуться обратно"
        ])
    elif choice == "Через подземные коммуникации":
        user_states[user_id] = STATES["underground"]
        text = "🕳️ Ты находишь аварийную шахту. Решётка закрыта, но ты можешь её вскрыть. Что будешь делать?"
        keyboard = get_keyboard([
            "Вскрыть решётку и проникнуть внутрь",
            "Использовать анализатор, чтобы проверить на наличие датчиков",
            "Использовать газ, если там сторожевые собаки",
            "Вернуться обратно"
        ])
    elif choice == "С крыши":
        user_states[user_id] = STATES["roof"]
        text = "🦅 Ты на крыше. Ниже — сигнализация и ангар. Как действовать?"
        keyboard = get_keyboard([
            "Проверить крышу с помощью дрона",
            "Включить блокиратор сигнализации",
            "Спуститься напрямую на верёвке",
            "Вернуться обратно"
        ])
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

    if choice in ["Использовать планшет для фальшивых прав", "Воспользоваться голосовым клонером", "Отвлечь внимание дроном-приманкой"]:
        bot.send_message(message.chat.id, "✅ Ты вошёл в здание.")
        user_states[user_id] = STATES["inside_building"]
        send_inside_building_options(message)
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

def handle_underground(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        user_states[user_id] = STATES["start"]
        start(message)
        return

    bot.send_message(message.chat.id, f"🔧 Ты выбрал: {choice}. Теперь ты внутри здания.")
    user_states[user_id] = STATES["inside_building"]
    send_inside_building_options(message)

def handle_roof(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        user_states[user_id] = STATES["start"]
        start(message)
        return

    bot.send_message(message.chat.id, f"🪂 Ты спускаешься внутрь через крышу.")
    user_states[user_id] = STATES["inside_building"]
    send_inside_building_options(message)

def send_inside_building_options(message):
    keyboard = get_keyboard([
        "Изучить данные на планшете",
        "Найти секретаря и получить информацию о графике Короны",
        "Проникнуть в серверную комнату",
        "Перейти к финальному этажу напрямую"
    ])
    bot.send_message(message.chat.id, "Выбери дальнейшее действие:", reply_markup=keyboard)

def handle_inside_building(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Изучить данные на планшете":
        bot.send_message(message.chat.id, "📊 На планшете маршрут Короны и слабые места в охране.")
    elif choice == "Найти секретаря и получить информацию о графике Короны":
        bot.send_message(message.chat.id, "📄 Секретарь рассказал: Корона будет один в 14:00.")
    elif choice == "Проникнуть в серверную комнату":
        user_states[user_id] = STATES["server_room_choice"]
        bot.send_message(message.chat.id, "🔒 Кодовый замок на серверной. Попробовать взломать?")
    elif choice == "Перейти к финальному этажу напрямую":
        handle_final_dialog(message)
    else:
        bot.send_message(message.chat.id, "❌ Неизвестное действие.")

def handle_server_room(message):
    user_id = message.from_user.id
    choice = message.text.lower()

    if "да" in choice or "взлом" in choice:
        bot.send_message(message.chat.id, "🔓 Взлом удался. Ты получил доступ.")
    else:
        bot.send_message(message.chat.id, "🚪 Ты не стал рисковать. Возвращаешься.")

    handle_final_dialog(message)

def handle_final_dialog(message):
    user_id = message.from_user.id
    user_states[user_id] = STATES["final_corona"]

    bot.send_message(message.chat.id,
        "👤 Ты встретил Корону. Он говорит:\n\n"
        "«Я не враг. Я внедрённый агент. Мои данные спасут страну. Ты готов мне поверить?»",
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
        "Устранить его немедленно": "💀 Ты выполнил приказ. Но теперь ты — следующая цель.",
        "Выслушать его": "⚖️ Он был нашим. Ты получил данные о предательстве.",
        "Забрать его с собой": "✅ Он выжил. Ты стал героем.",
        "Оставить его в покое": "🔍 Ты решил расследовать всё сам. Вперёд."
    }

    result = endings.get(choice)
    if result:
        bot.send_message(message.chat.id, result)
        bot.send_message(message.chat.id, "🔚 Игра окончена. Спасибо за прохождение!",
                         reply_markup=types.ReplyKeyboardRemove())
        user_states[user_id] = STATES["end_game"]
    else:
        bot.send_message(message.chat.id, "❌ Неизвестный выбор. Попробуй снова.")

# Запуск
bot.polling(none_stop=True)
