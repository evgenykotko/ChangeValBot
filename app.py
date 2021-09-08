import telebot
from config import keys, TOKEN
from extensions import ConversionExeption, ValConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message:telebot.types.Message):
    text = "Чтобы начать работу введите команду в формате: \n<имя вылюты> \
<в какую валюту перевести> \ <количество переводимой валюты>.\n Список доступных валют /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message:telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types="text")
def converter(message:telebot.types.Message):
    values = message.text.split(" ")
    try:
        if len(values) > 3:
            raise ConversionExeption("Избыточное количество параметров для конвертации")
        elif len(values) < 3:
            raise ConversionExeption("Нехватает параметров для конвертации")
        quote, base, amount = values
        total_base = ValConverter.convert(quote, base, amount)
    except ConversionExeption as e:
        bot.reply_to(message, f"Ошибка пользователя \n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:
        text = f"Цена {amount} {base} - {float(total_base)*float(amount)} {quote}"
        bot.send_message(message.chat.id, text)

bot.polling()

