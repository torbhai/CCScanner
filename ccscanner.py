from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

def extract_card_details(text):
    # A more robust regex pattern that accounts for different card number formats
    card_number_pattern = r'(\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b)'
    # A pattern for expiry date that considers various prefixes and separators
    expiry_date_pattern = r'\b(?:exp\.?|EXP\.?|expiration|EXPIRATION)\s*:?[-\s*]?\s*([0-1]?\d[-\/]\d{2,4})\b'
    # A pattern for CVV that considers various prefixes and possible separators
    cvv_pattern = r'\b(?:cvv|CVV|Cvv|security code|SECURITY CODE|code)\s*:?[-\s*]?(\d{3,4})\b'

    card_numbers = re.findall(card_number_pattern, text)
    expiry_dates = re.findall(expiry_date_pattern, text, re.IGNORECASE)
    cvvs = re.findall(cvv_pattern, text, re.IGNORECASE)

    # Sanitize and format the found details
    cards = []
    for i, card_number in enumerate(card_numbers):
        if i < len(expiry_dates) and i < len(cvvs):
            # Remove any non-digit characters from card number
            clean_card_number = re.sub(r'\D', '', card_number)
            # Ensure the expiry date is in the format MMYY
            expiry_date = expiry_dates[i].replace('/', '').replace('-', '')
            if len(expiry_date) == 3:  # Pad single-digit month with a zero
                expiry_date = '0' + expiry_date
            if len(expiry_date) == 6:  # Convert YYYY to YY
                expiry_date = expiry_date[:2] + expiry_date[4:]
            # Get the CVV
            cvv = cvvs[i]
            cards.append(f'{clean_card_number}|{expiry_date}|{cvv}')

    return cards

def format_card_details(update: Update, context: CallbackContext) -> None:
    card_details = extract_card_details(update.message.text)
    message = '\n'.join(card_details) if card_details else 'No valid card details found.'
    update.message.reply_text(message)

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your Bot's API token
    updater = Updater("6759397107:AAHjYMEyaauDyFVjkiT2Zq8B3hMTNvzJus0", use_context=True)

    dispatcher = updater.dispatcher

    # Add a message handler for the format_card_details function
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, format_card_details))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
