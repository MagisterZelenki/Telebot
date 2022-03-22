import telebot
from TeleBot import TOKEN, keys
from utilits import ConvertionException, MoneyConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'чтобы начать работу введите комманду боту в следующем формате: \n<название валюты> ' \
'<в какую валюту перевести> ' \
'<количество валюты> \n чтобы увидеть список всех доступных валют введите: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('должно быть 3 параметра')

        quote, base, amount = values
        total_base = (json.loads(r.content)[keys[base]] * float(amount)) #total_base = MoneyConvertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя: \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()