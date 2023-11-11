import os
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()

tg_bot_token = os.environ['TG_BOT_TOKEN']

messages = [{
    "role": "system",
    "content": "You are a helpful assistant that answers questions."
}]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot please talk to me!")

async def scrumples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_dice(chat_id=update.effective_chat.id)



if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler('start', start)
    scrumple_handler = CommandHandler('scrumples', scrumples)

    application.add_handler(start_handler)
    application.add_handler(scrumple_handler)

    application.run_polling()