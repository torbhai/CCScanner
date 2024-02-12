from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

def extract_card_details(text):
    card_details = []
    lines = text.split('\n')

    for i, line in enumerate(lines):
        # Regex pattern to match card numbers
        card_number_match = re.search(r'\b(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})\b', line)
        if card_number_match:
            card_number = card_number_match.group(1).replace(' ', '').replace('-', '')
            # Initialize expiry_date and cvv in case they are not found in the next two lines
            expiry_date, cvv = None, None
            # Look ahead in the next two lines for expiry date and CVV
            for j in range(1, 3):
                if i+j < len(lines):
                    next_line = lines[i+j]
                    # Regex pattern for expiry date if it has not been found yet
                    if not expiry_date:
                        expiry_date_match = re.search(r'\b([0-1]?\d[-\/]\d{2,4})\b', next_line)
                        if expiry_date_match:
                            expiry_date = expiry_date_match.group(1).replace('/', '').replace('-', '')
                            if len(expiry_date) == 3:  # Pad single-digit month with zero
                                expiry_date = '0' + expiry_date
                            if len(expiry_date) == 6:  # Convert four-digit year to two digits
                                expiry_date = expiry_date[:2] + expiry_date[4:]
                    # Regex pattern for CVV if it has not been found yet
                    if not cvv:
                        cvv_match = re.search(r'\b(\d{3,4})\b', next_line)
                        if cvv_match:
                            cvv = cvv_match.group(1)
            # If both expiry date and CVV have been found, append the details
            if expiry_date and cvv:
                card_details.append(f'{card_number}|{expiry_date}|{cvv}')

    return card_details

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
