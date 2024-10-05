from telegram_bot import TelegramBot


def lambda_handler(event, context):

    bot = TelegramBot(event)

    return bot.process_event()
