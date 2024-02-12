from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

def format_card_details(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.split("\n")

    card_number_pattern = r'\b\d{4} \d{4} \d{4} \d{4}\b'
    expiry_date_pattern = r'\b\d{2}[-/]\d{2}\b'  # updated to handle '-' or '/' as separators.
    cvv_pattern = r'(?i)cvv[-\s]\d{3,4}\b'  # updated to handle 'CVV-' or 'cvv ' as prefixes.

    card_numbers = re.findall(card_number_pattern, update.message.text)
    expiry_dates = re.findall(expiry_date_pattern, update.message.text)
    cvvs = re.findall(cvv_pattern, update.message.text)

    if len(card_numbers) == len(expiry_dates) == len(cvvs):
        formatted_cards = []
        for i in range(len(card_numbers)):
            card_number = card_numbers[i].replace(' ', '')
            expiry_date = expiry_dates[i].replace('/', '').replace('-', '')
            cvv = cvvs[i].split(' ')[1] if ' ' in cvvs[i] else cvvs[i].split('-')[1]
            formatted_cards.append(f'{card_number} | {expiry_date} | {cvv}')
        message = '\n'.join(formatted_cards)
    else:
        message = 'Invalid input. Please ensure your input includes a 16-digit card number, a 4-digit expiry date, and a 3 or 4-digit CVV for each card.'

    update.message.reply_text(message)

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your Bot's API token
    updater = Updater("6759397107:AAHjYMEyaauDyFVjkiT2Zq8B3hMTNvzJus0", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, format_card_details))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
