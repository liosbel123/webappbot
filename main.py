import json
import logging
import os
import requests

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def start(update: Update, context: CallbackContext):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    text = "This bot has a button to Open Google"
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Open Google",
                    "web_app": {"url": "https://google.com"}
                }
            ]
        ]
    }
    response = requests.post(
        url=url,
        data={"chat_id": update.effective_chat.id, "text": text, "reply_markup": json.dumps(keyboard)}
    )
    logger.info(response.text)


def main():
    # Create the Updater and pass it your bots token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()

    logger.info(f"Bot running on https://t.me/{dispatcher.bot.username}")

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
