import telebot
from telebot import types  # Теперь всё работает!

bot = telebot.TeleBot("YOUR_BOT_API_TOKEN_HERE")
# Хранение состояний пользователей
user_states = {}  # {user_id: current_state}

# Возможные состояния
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

# Инвентарь пользователя
user_inventory = {}  # {user_id: [items]}

# Предметы
ITEMS = [
    "Планшет",
    "Газовая капсула",
    "Маскировочный костюм M3",
    "Голосовой клонер",
    "Дрон-приманка",
]

# Кнопки
def get_keyboard(options):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        markup.add(telebot.types.KeyboardButton(option))
    return markup


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = STATES["start"]
    user_inventory[user_id] = ITEMS.copy()  # Добавляем все предметы в инвентарь

    welcome_text = (
        "👁️ Приветствую, Агент Ноль.\n\n"
        "Твоя миссия — устранить или обезвредить объект по имени \"Корона\". Он скрывается в административной башне \"Этернис\".\n\n"
        "У тебя есть доступ к следующим инструментам:\n"
        "- Планшет с картой и базами данных\n"
        "- Газовая капсула (парализует на короткое время)\n"
        "- Маскировочный костюм M3\n"
        "- Голосовой клонер\n"
        "- Дрон-приманка\n\n"
        "🔍 Выбери путь проникновения:"
    )

    keyboard = get_keyboard(["Через офисную зону", "Через подземные коммуникации", "С крыши"])
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


# Обработка выбора точки проникновения
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES["start"])
def choose_entry_point(message):
    user_id = message.from_user.id
    choice = message.text

    if choice not in ["Через офисную зону", "Через подземные коммуникации", "С крыши"]:
        bot.reply_to(message, "Пожалуйста, выбери один из предложенных вариантов.")
        return

    if choice == "Через офисную зону":
        user_states[user_id] = STATES["office_zone"]
        text = (
            "🪪 Ты подходишь к главному входу. На тебе маскировочный костюм M3, адаптированный под униформу технической службы.\n"
            "Охранник проверяет документы. Что будешь делать?"
        )
        buttons = [
            "Использовать планшет для фальшивых прав",
            "Воспользоваться голосовым клонером",
            "Отвлечь внимание дроном-приманкой",
            "Вернуться обратно"
        ]

    elif choice == "Через подземные коммуникации":
        user_states[user_id] = STATES["underground"]
        text = (
            "🕳️ Ты находишь аварийную шахту. Решётка закрыта, но ты можешь её вскрыть. Внутри темно.\n"
            "Что будешь делать?"
        )
        buttons = [
            "Вскрыть решётку и проникнуть внутрь",
            "Использовать анализатор, чтобы проверить на наличие датчиков",
            "Использовать газ, если там сторожевые собаки",
            "Вернуться обратно"
        ]

    elif choice == "С крыши":
        user_states[user_id] = STATES["roof"]
        text = (
            "🦅 Ты забираешься на крышу административной башни. Внизу виден вертолётный ангар и сигнализационные датчики.\n"
            "Как спуститься?"
        )
        buttons = [
            "Проверить крышу с помощью дрона",
            "Включить блокиратор сигнализации",
            "Спуститься напрямую на верёвке",
            "Вернуться обратно"
        ]

    keyboard = get_keyboard(buttons)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


# Обработка офисной зоны
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES["office_zone"])
def office_zone_choice(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Вернуться обратно":
        user_states[user_id] = STATES["start"]
        start(message)
        return

    if choice == "Использовать планшет для фальшивых прав":
        bot.reply_to(message, "✅ Ты успешно вошёл внутрь. Теперь ты внутри здания.")

    elif choice == "Воспользоваться голосовым клонером":
        bot.reply_to(message, "✅ Ты воспроизвёл пароль дня. Охранник пропустил тебя.")

    elif choice == "Отвлечь внимание дроном-приманкой":
        bot.reply_to(message, "✅ Ты запустил дрон. Охрана отвлечена. Ты прошёл внутрь.")

    else:
        bot.reply_to(message, "❌ Неизвестное действие.")
        return

    buttons = [
        "Изучить данные на планшете",
        "Найти секретаря и получить информацию о графике Короны",
        "Проникнуть в серверную комнату",
        "Перейти к финальному этажу напрямую"
    ]
    keyboard = get_keyboard(buttons)
    bot.send_message(message.chat.id, "Выбери дальнейшее действие:", reply_markup=keyboard)
    user_states[user_id] = STATES["inside_building"]


# Внутри здания
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES["inside_building"])
def inside_building_choice(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Изучить данные на планшете":
        bot.reply_to(message, "📊 Ты изучаешь данные. Узнал маршрут передвижения Короны и слабые места системы безопасности.")

    elif choice == "Найти секретаря и получить информацию о графике Короны":
        bot.reply_to(message, "📄 Секретарь сообщил тебе точное расписание Короны. Он будет один в 14:00.")

    elif choice == "Проникнуть в серверную комнату":
        bot.send_message(message.chat.id, "🔒 Ты приближаешься к серверной. На двери кодовый замок.")
        bot.send_message(message.chat.id, "Попробуешь взломать?")
        user_states[user_id] = STATES["server_room_choice"]
        return

    elif choice == "Перейти к финальному этажу напрямую":
        final_corona_dialog(message)
        return

    else:
        bot.reply_to(message, "❌ Неизвестное действие.")
        return

    bot.send_message(message.chat.id, "Выбери следующее действие:", reply_markup=get_keyboard([
        "Изучить данные на планшете",
        "Найти секретаря и получить информацию о графике Короны",
        "Проникнуть в серверную комнату",
        "Перейти к финальному этажу напрямую"
    ]))


# Серверная комната
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES["server_room_choice"])
def server_room_choice(message):
    user_id = message.from_user.id
    choice = message.text.lower()

    if "да" in choice or "взлом" in choice:
        bot.reply_to(message, "🔓 Ты успешно взломал систему. Отключил камеры и получил дополнительный доступ.")
        bot.reply_to(message, "Теперь ты можешь беспрепятственно пройти к Короне.")
    else:
        bot.reply_to(message, "🚫 Ты решил не рисковать. Возвращаешься к основному маршруту.")

    final_corona_dialog(message)


# Диалог с Короной
def final_corona_dialog(message):
    user_id = message.from_user.id
    user_states[user_id] = STATES["final_corona"]

    text = (
        "👤 Ты входишь в кабинет Короны. Он один. Он говорит:\n\n"
        "«Я знаю, кто ты. Я не враг. Я был направлен внутрь, чтобы собрать доказательства предательства. Мои данные могут спасти нас всех. Ты готов мне поверить?»\n\n"
        "Как ты поступишь?"
    )

    buttons = [
        "Устранить его немедленно",
        "Выслушать его",
        "Забрать его с собой",
        "Оставить его в покое"
    ]

    bot.send_message(message.chat.id, text, reply_markup=get_keyboard(buttons))


# Обработка финального выбора
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES["final_corona"])
def final_choice(message):
    user_id = message.from_user.id
    choice = message.text

    if choice == "Устранить его немедленно":
        bot.send_message(message.chat.id, "💀 Ты выполнил приказ. Корона мёртв. Цель достигнута.\n\nНо в базе данных ты находишь файлы, которые говорят о твоём собственном устранении...\n\nТы стал частью машины... пока она не обратилась к тебе.")

    elif choice == "Выслушать его":
        bot.send_message(message.chat.id, "⚖️ Ты выслушал Корону. Оказалось, он был наш человек. Он дал тебе доказательства измены руководства.\n\nТеперь ты должен принять решение…")

    elif choice == "Забрать его с собой":
        bot.send_message(message.chat.id, "✅ Ты вывел Корону. Он доказал свою невиновность. Теперь ты герой.\n\nТы выбрал путь разума. Мир стал немного лучше.")

    elif choice == "Оставить его в покое":
        bot.send_message(message.chat.id, "🔍 Ты оставил Корону одного. Пора начать своё расследование...\n\nТы доверил фактам больше, чем приказам.")

    else:
        bot.reply_to(message, "❌ Неизвестное действие.")
        return

    bot.send_message(message.chat.id, "🔚 Игра окончена. Спасибо за прохождение!", reply_markup=types.ReplyKeyboardRemove())
    user_states[user_id] = STATES["end_game"]


# Запуск бота
bot.polling(none_stop=True)
