from telebot import TeleBot, types
from database import initialize_database, add_user, delete_user, get_subscribed_users
from horoscope import generate_horoscope
from scheduler import start_scheduler
from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)


def send_horoscope_to_users():
    users = get_subscribed_users()
    for user_id, zodiac_sign in users:
        horoscope = generate_horoscope()
        try:
            bot.send_message(user_id, f"Ваш гороскоп на сегодня ({zodiac_sign}):\n\n{horoscope}")
        except Exception as e:
            print(f"Ошибка отправки пользователю {user_id}: {e}")


@bot.message_handler(commands=['start'])
def start_message(message):
    # Удаляем старую клавиатуру
    bot.send_message(
        message.chat.id,
        "Обновляем клавиатуру...",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Создаём новую клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("Гороскоп на сегодня"),
        types.KeyboardButton("Подписаться на гороскоп"),
        types.KeyboardButton("Отписаться")
    )

    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите действие:\n"
        "1. 'Гороскоп на сегодня' — посмотреть гороскоп сейчас (или отправьте '1').\n"
        "2. 'Подписаться на гороскоп' — получать гороскоп ежедневно (или отправьте '2').\n"
        "3. 'Отписаться' — прекратить подписку на гороскопы (или отправьте '3').",
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_input = message.text.strip()

    if user_input in ["Гороскоп на сегодня", "1"]:
        # Создаём инлайн-клавиатуру с выбором знаков зодиака
        zodiac_keyboard = types.InlineKeyboardMarkup()
        zodiac_signs = [
            'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
            'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
        ]
        for sign in zodiac_signs:
            zodiac_keyboard.add(
                types.InlineKeyboardButton(text=sign, callback_data=f"Гороскоп на сегодня:{sign}")
            )
        bot.send_message(
            message.chat.id,
            "Выберите ваш знак зодиака:",
            reply_markup=zodiac_keyboard
        )

    elif user_input in ["Подписаться на гороскоп", "2"]:
        # Создаём инлайн-клавиатуру с выбором знаков зодиака
        zodiac_keyboard = types.InlineKeyboardMarkup()
        zodiac_signs = [
            'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
            'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
        ]
        for sign in zodiac_signs:
            zodiac_keyboard.add(
                types.InlineKeyboardButton(text=sign, callback_data=f"Подписаться на гороскоп:{sign}")
            )
        bot.send_message(
            message.chat.id,
            "Выберите ваш знак зодиака для подписки:",
            reply_markup=zodiac_keyboard
        )

    elif user_input in ["Отписаться", "3"]:
        # Отписка пользователя
        delete_user(message.chat.id)
        bot.send_message(
            message.chat.id,
            "Вы успешно отписались от рассылки гороскопов."
        )

    elif user_input == "/help":
        # Помощь пользователю
        bot.send_message(
            message.chat.id,
            "Команды:\n"
            "1. '1' или 'Гороскоп на сегодня' — посмотреть гороскоп.\n"
            "2. '2' или 'Подписаться на гороскоп' — подписаться на ежедневные гороскопы.\n"
            "3. '3' или 'Отписаться' — отменить подписку на гороскопы.\n"
        )

    else:
        # Обработка неизвестного ввода
        bot.send_message(
            message.chat.id,
            "Я вас не понимаю. Нажмите /help для подсказки."
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_zodiac_callback(call):
    # Обработка выбора знака зодиака
    action, zodiac_sign = call.data.split(":")

    if action == "Гороскоп на сегодня":
        horoscope = generate_horoscope()
        bot.send_message(call.message.chat.id, f"Ваш гороскоп на сегодня ({zodiac_sign}):\n\n{horoscope}")
    elif action == "Подписаться на гороскоп":
        add_user(call.message.chat.id, call.message.chat.username, zodiac_sign)
        bot.send_message(call.message.chat.id, f"Вы успешно подписались на гороскоп для знака {zodiac_sign}!")


if __name__ == "__main__":
    initialize_database()
    start_scheduler(send_horoscope_to_users, "10:00")
    bot.polling(none_stop=True)
