# importing the necessary modules

import os
import random
import telebot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import InputTextMessageContent
from telebot.types import InlineQueryResultCachedSticker

API_KEY = os.getenv("API-KEY")      # API TOKEN from @BotFather

# storing the file_ids from Telegram servers

BANNER = "AgACAgUAAxkBAAMDYoeu5WbkziZdcibcP9llPILJS_\
kAAjK0MRtvCkFUmAmFH6vvxjkBAAMCAAN5AAMkBA"
COIN = "CAACAgIAAxkBAAMJYoexj1eJxVQY0R98jqcX0ZaQqhwA\
Ar4JAAKErphKEkME6E2wM7IkBA"
HEADS = "CAACAgUAAxkBAAMHYoewFSFllpNDI2suypkk2H3DaRsA\
AkYFAALwJzFU0tHe9ydf8jgkBA"
TAILS = "CAACAgUAAxkBAAMIYoewMk78FlKO_5xAAr38_r9KCQwA\
Ai8GAAIBWDBUh_A_KXLBzrUkBA"

art = [                     # stylish fonts for heads and tails
"""<code>\
█░░█ █▀▀ █▀▀█ █▀▀▄ █▀▀
█▀▀█ █▀▀ █▄▄█ █░░█ ▀▀█
▀░░▀ ▀▀▀ ▀░░▀ ▀▀▀░ ▀▀▀
</code>"""
,
"""<code>\
▀▀█▀▀ █▀▀█ ░▀░ █░░ █▀▀
░░█░░ █▄▄█ ▀█▀ █░░ ▀▀█
░░▀░░ ▀░░▀ ▀▀▀ ▀▀▀ ▀▀▀
</code>"""
]

bot = telebot.TeleBot(API_KEY, parse_mode="HTML")   # Initializing the bot

def flip():             # Defining a toss function using random module
    coin = {0: ["HEADS", HEADS], 1: ["TAILS", TAILS]}
    return coin[random.choice([0, 1])]

@bot.message_handler(commands="start")      # /start command
def start(message):

    bot.send_photo(message.chat.id, BANNER, caption="<b>Can't seem to decide on something?\n\
    \nLet me help you! 😄\n\nChoose Heads or Tails and press /toss.\n\
    \nYou can also use me in other chats too!\n\nJust tag @tossflipbot and toss! 😉</b>",
    reply_markup = InlineKeyboardMarkup().row(InlineKeyboardButton(
        "Try me in other chats! 💬", switch_inline_query="")))

@bot.message_handler(commands="toss")   # /toss command
def toss(message):

    bot.send_sticker(message.chat.id, COIN, reply_markup = InlineKeyboardMarkup().row(
        InlineKeyboardButton("Flip a coin! 🪙", callback_data="toss")))

@bot.inline_handler(lambda query: True)     # Inline Mode for any chat
def toss_inline(query):

    try:
        value = random.randint(0, 1)

        if not value:
            score = "1-0"
            counter_button = InlineKeyboardButton(
                "|| HEADS - 1 || TAILS - 0 ||", callback_data="score")
        else:
            score = "0-1"
            counter_button = InlineKeyboardButton(
                "|| HEADS - 0 || TAILS - 1 ||", callback_data="score")

        toss = InlineQueryResultCachedSticker(f'toss-{random.randint(0, 1)}', COIN,
            reply_markup= InlineKeyboardMarkup(row_width=1).add(*[counter_button, InlineKeyboardButton(
                "Flip again! 🪙", callback_data=f"toss-inline::{score}")]),
                input_message_content=InputTextMessageContent(art[value], parse_mode="HTML"))
        bot.answer_inline_query(query.id, [toss])

    except: pass

@bot.callback_query_handler(func=lambda call: call.data[:11] == 'toss-inline')
def callback_listener(call):        # Handles all the inline callbacks

    inline_id, score = call.data.split("::")

    heads, tails = map(int, score.split("-"))
    value = random.randint(0, 1)

    if not value:
        score = f"{heads+1}-{tails}"
        counter_button = InlineKeyboardButton(
            f"|| HEADS - {heads+1} || TAILS - {tails} ||", callback_data="score")
    else:
        score = f"{heads}-{tails+1}"
        counter_button = InlineKeyboardButton(
            f"|| HEADS - {heads} || TAILS - {tails+1} ||", callback_data="score")

    bot.edit_message_text(art[value], inline_message_id=call.inline_message_id,
        reply_markup=InlineKeyboardMarkup(row_width=1).add(*[
            counter_button, InlineKeyboardButton("Flip again! 🪙",
            callback_data=f"toss-inline::{score}")]))       

@bot.callback_query_handler(func=lambda call: call.data == 'toss')
def callback_listener(call):        # Handles all the private chat callbacks

    result = flip()
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_sticker(call.message.chat.id, result[-1], reply_markup=InlineKeyboardMarkup(
        row_width=1).add(*[InlineKeyboardButton(result[0], callback_data=result[0]),
        InlineKeyboardButton("Flip again! 🪙", callback_data="toss")]))

bot.infinity_polling(           # Starts the polling
    skip_pending=True)
