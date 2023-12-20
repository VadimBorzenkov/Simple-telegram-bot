import telebot
from telebot import types
import config
import sys
import requests
from io import BytesIO


bot = telebot.TeleBot(config.TOKEN) # Создание бота по токену
audio_url = "https://github.com/VadimBorzenkov/Laba1/raw/master/audio.mp3"
photo_url = "https://github.com/VadimBorzenkov/Laba1/raw/master/photo1.png"


def send_keyboard(message):
    markup = types.InlineKeyboardMarkup()
    # Кнопка для отправки фото
    photo_btn = types.InlineKeyboardButton(
        "Покажи картинку", callback_data="send_photo")

    # Кнопка для отправки аудио
    audio_btn = types.InlineKeyboardButton(
        "Отправь аудио", callback_data="send_audio")
    markup.row(photo_btn, audio_btn)

    bot.send_message(
        message.chat.id, "Выберите действие", reply_markup=markup)


def main():
    @bot.message_handler(commands=['start']) # Обработчик сообщения /start
    def start(message):
        send_keyboard(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        if call.data == "send_photo":
            try:
                # Отправляем GET-запрос для скачивания фото
                response = requests.get(photo_url)
                
                if response.status_code == 200:
                    # Преобразуем полученные байты в файл
                    photo_file = BytesIO(response.content)
                    
                    # Отправляем фото в чат
                    bot.send_photo(call.message.chat.id, photo_file)
                else:
                    bot.send_message(call.message.chat.id, "Не удалось загрузить фото.")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")

        elif call.data == "send_audio":
            try:
                # Отправляем GET-запрос для скачивания фото
                response = requests.get(audio_url)
                
                if response.status_code == 200:
                    # Преобразуем полученные байты в файл
                    audio_file = BytesIO(response.content)
                    
                    # Отправляем фото в чат
                    bot.send_audio(call.message.chat.id, audio_file)
                else:
                    bot.send_message(call.message.chat.id, "Не удалось загрузить аудио.")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")



        # Повторный показ конопок после обработки запроса
        send_keyboard(call.message)


    @bot.message_handler(func=lambda message: message.text.lower() == "ссылка на гит") # Обработчик сообщения "ссылка на гит"
    def info(message):
        bot.send_message(message.chat.id, 'https://github.com/VadimBorzenkov/Laba1')
        send_keyboard(message)
        
    # @bot.message_handler(commands=['stop']) # Обработчик команды "/stop"
    def stop(message):
        # Отправляем сообщение о завершении работы
        bot.send_message(message.chat.id, "Бот остановлен.")
        
        # Останавливаем бота
        bot.stop_polling()
        
    bot.message_handler(commands=['stop'])(stop) # Аналогичный обработчки команды "/stop"
        
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()