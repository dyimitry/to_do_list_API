import os

from telebot import types

import telebot
# from dotenv import load_dotenv

from telegram_bot.client import TodoCleint

# load_dotenv()

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)

host = os.getenv("BOT_BACKEND_HOST")
port = os.getenv("BOT_BACKEND_PORT")
clientDB = TodoCleint(host=host, port=int(port))

pred_message = ''


@bot.message_handler(commands=['start'])
def start(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    result = clientDB.registration(us_id, us_name, us_sname, username)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="Создать новую задачу", callback_data="create_task"))
    markup.add(types.InlineKeyboardButton(
        text="Показать мои задачи", callback_data="get_tasks"))

    bot.send_message(
        message.chat.id,
        text=f"Привет, {message.from_user.first_name}! Не запоминай все, записывай в меня и я тебе напомню!",
        reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "create_task")
def button_pressed_handler(call):
    bot.send_message(
        chat_id=call.message.chat.id,
        text="Напишите свою задачу в формате:\n"
             "Создать задачу\n"
             "Название задачи: «Необходимо написать»\n"
             "Описание задачи: «Необходимо написать»\n"
             "Срочность задачи: «Не срочно»/«Срочно»/«Очень срочно»")


@bot.callback_query_handler(func=lambda call: call.data == "get_tasks")
def button_pressed_handle(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="Изменить задачу", callback_data="update_task"))
    markup.add(types.InlineKeyboardButton(
        text="Удалить задачу", callback_data="delete_task"))
    user_id = call.from_user.id
    result = clientDB.get_tasks(user_id)

    stroka = ''
    for i in result:
        stroka += f"Задача: №{i['id']}, Название задачи:{i['name']}, Описание задачи:{i['description']}, Статус:{i['status']}, Срочность:{i['urgency']}\n"
    bot.send_message(
        call.message.chat.id,
        text=stroka,
        reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "delete_task")
def button_pressed_hand(call):
    bot.send_message(
        call.message.chat.id,
        text="Введите  номер задачи, которую Вы хотите удалить (числом)",
    )


@bot.callback_query_handler(func=lambda call: call.data == "da")
def button_pressed_hand(call):
    text = call.json["message"]["text"]
    res = text.split(':')[-1].strip("?")

    clientDB.delete_task(res)
    bot.send_message(
        call.message.chat.id,
        text="Задача успешо удалена",
    )


# @bot.callback_query_handler(func=lambda call: call.data == "enter_number")
# def button_pressed_handle(call):
#         # Удалить задачу написав в тг ее id
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton(
#         text="Да", callback_data="da"))
#     markup.add(types.InlineKeyboardButton(
#         text="Нет", callback_data="no"))
# if call.message.text.isdigit():
#     # result = clientDB.delete_task(call.message.text)
#     bot.send_message(
#         call.message.chat.id,
#         text=f"Вы точно хотите удалить задачу {call.message.text}?")
#     if len(result) == 1:
#         stroka = result['detail']
#         bot.send_message(
#             call.message.chat.id,
#             text=stroka)
#         return
#     stroka = (f"Задача: №{result['id']}. Название задачи:{result['name']}.\n"
#               f"Успешно удалена")
#     bot.send_message(
#         call.message.chat.id,
#         text=stroka)

@bot.message_handler(content_types=['text'])
def function(message):
    # if message.text == "Создать новую задачу":
    #     bot.send_message(
    #         message.chat.id,
    #         text="Напишите свою задачу в формате:\n"
    #              "Создать задачу\n"
    #              "Название задачи: «Необходимо написать»\n"
    #              "Описание задачи: «Необходимо написать»\n"
    #              "Срочность задачи: «Не срочно»/«Срочно»/«Очень срочно»")

    # if message.text == "Показать мои задачи":
    #     markup = types.InlineKeyboardMarkup()
    #     markup.add(types.InlineKeyboardButton(
    #         text="Изменить задачу", callback_data="update_task"))
    #     markup.add(types.InlineKeyboardButton(
    #         text="Удалить задачу", callback_data="delete_tasks"))
    #     # btn1 = types.InlineKeyboardButton(text="Изменить задачу", callback_data="update_task")
    #     # btn2 = types.InlineKeyboardButton(text="Удалить задачу", callback_data="delete_tasks")
    #     # markup.add(btn1, btn2)
    #     user_id = message.from_user.id
    #     result = clientDB.get_tasks(user_id)
    #
    #     stroka = ''
    #     for i in result:
    #         stroka += f"Задача: №{i['id']}, Название задачи:{i['name']}, Описание задачи:{i['description']}, Статус:{i['status']}, Срочность:{i['urgency']}\n"
    #     bot.send_message(
    #         message.chat.id,
    #         text=stroka,
    #         reply_markup=markup)

    # if message.text == "Удалить задачу":
    #     bot.send_message(
    #         message.chat.id,
    #         text="Напишите номер задачи которую необходимо удалить (числом)")
    # Удалить задачу написав в тг ее id
    if message.text.isdigit():
        # result = clientDB.delete_task(message.text)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text="Да", callback_data="da"))
        markup.add(types.InlineKeyboardButton(
            text="Нет", callback_data="no"))
        result = clientDB.get_task(message.text)
        if len(result) == 0:
            bot.send_message(
                message.chat.id,
                text="Такой задачи не существует")
            return
        bot.send_message(
            message.chat.id,
            text=f"Подтвердите что хотите удалить задачу №:{message.text}?",
            reply_markup=markup)
        task_delete=message.text
        return task_delete
        # if len(result) == 1:
        #     stroka = result['detail']
        #     bot.send_message(
        #         message.chat.id,
        #         text=stroka)
        #     return
        # stroka = (f"Задача: №{result['id']}. Название задачи:{result['name']}.\n"
        #           f"Успешно удалена")

    if message.text == "Изменить задачу":
        bot.send_message(
            message.chat.id,
            text="Если Вы хотите изменить статус задачи,\n"
                 "Необходимо передать новые данные в формате:\n"
                 "Задача №:«Необходимо написать»\n"
                 "Статус: «Необходимо написать»")
    # ИЗМЕНИТЬ ЗАДАЧУ
    if message.text.startswith("Задача №"):
        if not message.text.startswith("Задача №:"):
            bot.send_message(
                message.chat.id,
                text='Необходимо установить «:» после №')
            return
        message_lines = message.text.split("\n")

        number = message_lines[0].split(":")[1].strip()
        if number.isdigit():
            status = message_lines[1].split(":")[1].strip()
            stat = None

            if status == "True":
                stat = True
            if stat is None:
                bot.send_message(
                    message.chat.id,
                    text='Если задача выполнена то нужно изменить статус на True без отспупа от «:»')
                return
            result_get_task = clientDB.get_task(number)
            if result_get_task.get('detail'):
                bot.send_message(
                    message.chat.id,
                    text=f"{result_get_task['detail']}")
                return
            name = result_get_task['name'].strip()
            description = result_get_task['description'].strip()
            result = clientDB.update_task(number, name, description, stat)
            bot.send_message(
                message.chat.id,
                text="Статус задачи успешно изменен")
            return
        bot.send_message(
            message.chat.id,
            text="Необходимо написать № числом")
    # СОЗДАТЬ ЗАДАЧУ
    if message.text.startswith("Создать задачу"):
        message_lines = message.text.split("\n")
        try:
            task_name = message_lines[1].split(":")[1].strip()
            task_descripton = message_lines[2].split(":")[1].strip()
            task_urgency = message_lines[3].split(":")[1].strip()
            user_id = message.from_user.id
            status = False

            result = clientDB.create_task(task_name, task_descripton, status, task_urgency, user_id)
            bot.send_message(
                message.chat.id,
                text='Задача успешно создана. Вы можете ее посмотреть в списке задач.')
        except:
            bot.send_message(
                message.chat.id,
                text='Необходимо установить «:»')
    if message.text == "q":
        user_id = message.from_user.id
        a = clientDB.get_tasks_status_false(user_id)
        c = 1
        bot.send_message(
            message.chat.id,
            text="Если Вы хотите изменить статус задачи,\n"
                 "Необходимо передать новые данные в формате:\n"
                 "Задача №:«Необходимо написать»\n"
                 "Статус: «Необходимо написать»")


bot.polling(none_stop=True)
