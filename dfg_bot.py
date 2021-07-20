import telebot
from telebot import types
import random

API_TOKEN = "token"

bot = telebot.TeleBot(API_TOKEN)

game_dict = {}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, '''Добро пожаловать в числовую угадайку
Укажите максимальное значение угадываемого числа: ''')
    bot.register_next_step_handler(msg, gener_num)

def is_valid(g):
    if g.isdigit():
        if 0 < int(g):
            return True
        else:
            return False
    else:
        return False

def gener_num(message):
    try:
        global game_dict
        game_dict[message.from_user.id] = {'mx': 0, 'n': 0}
        game_dict['counts'] = 0
        chat_id = message.chat.id
        mx = message.text
        if is_valid(mx):
            n = random.randint(1, int(mx))
            msg = bot.send_message(chat_id, f'''Число загадано
Отгадайте загаданное число от 1 до {mx}:''')
            game_dict['mx'] = mx
            game_dict['n'] = n
            bot.register_next_step_handler(msg, the_game)
        else:
            bot.reply_to(message, 'это не цифра, начинай всё сначала')
    except Exception as e:
        bot.reply_to(message, 'oooops, start again')

def the_game(message):
    try:
        global game_dict
        n = game_dict['n']
        g = message.text
        game_dict['counts'] += 1
        if is_valid(g):
            if int(g) < n:
                msg = bot.reply_to(message, "Ваше число меньше загаданного, попробуйте еще разок")
                bot.register_next_step_handler(msg, the_game)
            elif int(g) > n:
                msg = bot.reply_to(message, "Ваше число больше загаданного, попробуйте еще разок")
                bot.register_next_step_handler(msg, the_game)
            elif int(g) == n:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add('Да', 'Нет')
                msg = bot.reply_to(message, f'''Вы угадали, поздравляем!
Вы отгадали с {game_dict['counts']} раза.
Хотите сыграть ещё?''', reply_markup=markup)
                bot.register_next_step_handler(msg, again)
    except Exception as e:
        bot.reply_to(message, 'oooops, try again')

def again(message):
    try:
        chat_id = message.chat.id
        answ = message.text
        if answ == 'Да':
            msg = bot.send_message(chat_id, '''Укажите максимальное значение угадываемого числа: ''')
            bot.register_next_step_handler(msg, gener_num)
        elif answ == 'Нет':
            msg = bot.send_message(chat_id, '''Спасибо, что играли в числовую угадайку. Еще увидимся...''')
        else:
            bot.reply_to(message, 'oooops, start again')
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
