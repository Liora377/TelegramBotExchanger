import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую Вас! \nЧтобы начать работу введите комманду боту в следующем формате: \n<название валюты> \
<в какую валюту перевести> <сумма переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
            text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Неверное количество параметров')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        sum = total_base * float(amount)
        text = f'Цена {amount} {quote} в {base} - {sum}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)