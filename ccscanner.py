from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

def format_card_details(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    card_number_pattern = r'\b\d{16}\b'
    expiry_date_pattern = r'\b\d{2}-\d{2}\b'
    cvv_pattern = r'\b\d{3}\b'

    card_number = re.search(card_number_pattern, user_input)
    expiry_date = re.search(expiry_date_pattern, user_input)
    cvv = re.search(cvv_pattern, user_input)

    if card_number and expiry_date and cvv:
        card_number = card_number.group()
        expiry_date = expiry_date.group().replace('-', '')
        cvv = cvv.group()
        message = f'{card_number} | {expiry_date} | {cvv}'
    else:
        message = 'Invalid input. Please ensure your input includes a 16-digit card number, a 4-digit expiry date, and a 3-digit CVV.'

    update.message.reply_text(message)

def main() -> None:
    # Replace 'TOKEN' with your Bot's API token
    updater = Updater("6759397107:AAHjYMEyaauDyFVjkiT2Zq8B3hMTNvzJus0", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, format_card_details))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
