from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

def extract_card_details(entry):
    card_number_match = re.search(r'(\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4})', entry)
    expiry_date_match = re.search(r'\bexp\.?\s*([0-1]?\d[/\-][0-9]{2,4})', entry, re.IGNORECASE)
    cvv_match = re.search(r'\b(?:cvv|CVV|Cvv)[-:\s]?\s*(\d{3,4})\b', entry)

    if card_number_match and expiry_date_match and cvv_match:
        card_number = card_number_match.group(1).replace(' ', '').replace('-', '')
        expiry_date = expiry_date_match.group(1).replace('/', '').replace('-', '')
        if len(expiry_date) == 3:  # Pad single-digit month with zero
            expiry_date = '0' + expiry_date
        if len(expiry_date) == 6:  # Convert four-digit year to two digits
            expiry_date = expiry_date[:2] + expiry_date[4:]
        cvv = cvv_match.group(1)
        return f'{card_number}|{expiry_date}|{cvv}'
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

    # Add a message handler for the format_card_details function
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, format_card_details))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
