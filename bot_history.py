import telebot

bot = telebot.TeleBot("YOUR_BOT_API_TOKEN_HERE")

# Хранение состояний пользователей
user_states = {}  # {user_id: current_state}

# Возможные состояния
STATES = {
    "start": "start",
    "choose_entry_point": "choose_entry_point",
    "office_zone": "office_zone",
    "underground": "underground",
    "roof": "roof"
}

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


# Заглушка для остальных шагов
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) in [STATES["underground"], STATES["roof"]])
def generic_step(message):
    bot.reply_to(message, f"Вы выбрали: {message.text}\nЭтот шаг ещё в разработке...")


# Запуск бота
bot.polling(none_stop=True)
