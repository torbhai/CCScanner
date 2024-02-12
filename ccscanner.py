from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

def extract_card_details(entry):
    card_number_match = re.search(r'\b(\d{4} \s\d{4} \s\d{4} \s\d{4})\b', entry)
    expiry_date_cvv_match = re.search(r'\b(\d{2}[/\-]\d{2,4})\s*(cvv[-\s]?|CVV[-\s]?)(\d{3,4})\b', entry, re.IGNORECASE)
    
    if card_number_match and expiry_date_cvv_match:
        card_number = card_number_match.group(1).replace(' ', '')
        expiry_date = expiry_date_cvv_match.group(1).replace('/', '').replace('-', '')
        cvv = expiry_date_cvv_match.group(3)
        return f'{card_number} | {expiry_date} | {cvv}'
    else:
        return None

def format_card_details(update: Update, context: CallbackContext) -> None:
    card_entries = update.message.text.strip().split('#')[1:]  # Split entries and remove the first empty entry

    formatted_cards = [extract_card_details(entry) for entry in card_entries]
    formatted_cards = [card for card in formatted_cards if card is not None]  # Filter out None values

    message = '\n'.join(formatted_cards) if formatted_cards else 'No valid card details found.'
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
