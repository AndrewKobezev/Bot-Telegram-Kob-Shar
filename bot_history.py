import os
import telebot
from telebot import types
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена. Убедись, что файл .env существует и содержит токен.")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Состояния пользователей
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
        "Твоя миссия — устранить или обезвредить объект по имени \"Корона\"...\n\n"
        "🔍 Выбери путь проникновения:"
    )
    keyboard = get_keyboard(["Через офисную зону", "Через подземные коммуникации", "С крыши"])
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES["start"])
def choose_entry_point(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Через офисную зону":
        user_states[user_id] = STATES["office_zone"]
        text = "🪪 Ты подходишь к главному входу. Охранник проверяет документы. Что будешь делать?"
        buttons = [
            "Использовать планшет для фальшивых прав",
            "Воспользоваться голосовым клонером",
            "Отвлечь внимание дроном-приманкой",
            "Вернуться обратно"
        ]

    elif choice == "Через подземные коммуникации":
        user_states[user_id] = STATES["underground"]
        text = "🕳️ Темно и узко. Что будешь делать?"
        buttons = [
            "Вскрыть решётку и проникнуть внутрь",
            "Использовать анализатор, чтобы проверить на наличие датчиков",
            "Использовать газ, если там сторожевые собаки",
            "Вернуться обратно"
        ]

    elif choice == "С крыши":
        user_states[user_id] = STATES["roof"]
        text = "🦅 На крыше. Видно вертолётную площадку. Что дальше?"
        buttons = [
            "Проверить крышу с помощью дрона",
            "Включить блокиратор сигнализации",
            "Спуститься напрямую на верёвке",
            "Вернуться обратно"
        ]

    else:
        bot.reply_to(message, "❌ Выбери один из предложенных вариантов.")
        return

    bot.send_message(message.chat.id, text, reply_markup=get_keyboard(buttons))


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == STATES["underground"])
def underground_choice(message):
    uid = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        start(message)
    else:
        bot.reply_to(message, f"🔍 Вы выбрали: {choice}. (здесь будет продолжение сцены)")


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == STATES["office_zone"])
def office_zone_choice(message):
    uid = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        start(message)
        return

    known_choices = {
        "Использовать планшет для фальшивых прав": "✅ Ты вошёл внутрь с фальшивыми правами.",
        "Воспользоваться голосовым клонером": "✅ Ты прошёл благодаря голосовому клонеру.",
        "Отвлечь внимание дроном-приманкой": "✅ Дрон сработал. Путь свободен."
    }

    if choice in known_choices:
        bot.reply_to(message, known_choices[choice])
        user_states[uid] = STATES["inside_building"]
        bot.send_message(message.chat.id, "Выбери дальнейшее действие:", reply_markup=get_keyboard([
            "Изучить данные на планшете",
            "Найти секретаря и получить информацию о графике Короны",
            "Проникнуть в серверную комнату",
            "Перейти к финальному этажу напрямую"
        ]))
    else:
        bot.reply_to(message, "❌ Неизвестное действие.")


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == STATES["inside_building"])
def inside_building_choice(message):
    uid = message.from_user.id
    choice = message.text

    if choice == "Изучить данные на планшете":
        bot.reply_to(message, "📊 Ты изучаешь маршрут Короны.")
    elif choice == "Найти секретаря и получить информацию о графике Короны":
        bot.reply_to(message, "📄 Секретарь дал расписание.")
    elif choice == "Проникнуть в серверную комнату":
        bot.send_message(message.chat.id, "🔒 У двери код. Взломать?")
        user_states[uid] = STATES["server_room_choice"]
    elif choice == "Перейти к финальному этажу напрямую":
        final_corona_dialog(message)
    else:
        bot.reply_to(message, "❌ Неизвестное действие.")


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == STATES["server_room_choice"])
def server_room_choice(message):
    uid = message.from_user.id
    choice = message.text.lower()

    if "да" in choice or "взлом" in choice:
        bot.reply_to(message, "🔓 Взлом успешен. Камеры отключены.")
    else:
        bot.reply_to(message, "🚫 Решил не рисковать.")

    final_corona_dialog(message)


def final_corona_dialog(message):
    uid = message.from_user.id
    user_states[uid] = STATES["final_corona"]

    text = (
        "👤 В кабинете Короны. Он говорит:\n"
        "«Я не враг. Я внедрённый агент. Доверься мне?»"
    )

    bot.send_message(message.chat.id, text, reply_markup=get_keyboard([
        "Устранить его немедленно",
        "Выслушать его",
        "Забрать его с собой",
        "Оставить его в покое"
    ]))


@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == STATES["final_corona"])
def final_choice(message):
    uid = message.from_user.id
    choice = message.text

    endings = {
        "Устранить его немедленно": "💀 Корона мёртв. Но ты — следующий.",
        "Выслушать его": "⚖️ Ты получил доказательства. Миссия усложнилась.",
        "Забрать его с собой": "✅ Вы ушли вместе. Истина восторжествовала.",
        "Оставить его в покое": "🔍 Ты ушёл один. Ответы остались в прошлом."
    }

    if choice in endings:
        bot.send_message(message.chat.id, endings[choice])
        bot.send_message(message.chat.id, "🔚 Игра окончена. Спасибо!", reply_markup=types.ReplyKeyboardRemove())
        user_states[uid] = STATES["end_game"]
    else:
        bot.reply_to(message, "❌ Неизвестное действие.")


# Старт бота
if __name__ == "__main__":
    print("🤖 Бот запущен.")
    bot.polling(none_stop=True)
