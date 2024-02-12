# CCScanner
# Credit Card Formatter Bot

## Introduction

The Credit Card Formatter Bot is a Telegram bot designed to simplify and standardize the presentation of credit card details. It uses text parsing techniques to extract key credit card details from user inputs and formats them in a clean, consistent manner.

## Features

- Extracts and formats 16-digit card numbers.
- Extracts and formats 4-digit expiry dates.
- Extracts and formats 3-digit CVVs.
- Provides error messages for invalid inputs.

## Usage

1. Send a message to the bot including a 16-digit card number, a 4-digit expiry date, and a 3-digit CVV. The bot will extract these details and format them as follows: `4117704081555319 | 0326 | 720`.

## Installation

This bot uses the python-telegram-bot library. You can install this library using pip:

```bash
pip install python-telegram-bot
```

## Running the Bot

Replace "TOKEN" in the script with your Bot's API token, and then run the script. The bot will start polling for updates.

## Disclaimer

This bot is designed for simplicity and ease of use and does not include any security measures. It should not be used to handle sensitive information without adding appropriate security features. Always respect and protect personal data in accordance with all relevant laws and regulations.

## Contributing

We always welcome contributions to help make our bot better. Please feel free to fork the repository and submit a pull request.

## License

This project is licensed under the terms of the MIT license.
