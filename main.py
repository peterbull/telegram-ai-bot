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

class LabeledPrice:
    def __init__(self, label: str, amount: float):
        self.label = label
        self.amount = amount

price1 = LabeledPrice("price1", 1.01)
price2 = LabeledPrice("price2", 2.04)
labeled_prices = [price1, price2]

async def scrumples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(chat_id=update.effective_chat.id,
                                   description="Mock invoice from Scrumples Inc.",
                                   payload="You owe Scrumples some money",
                                   currency="USD",
                                   prices=labeled_prices
                                   )
    

    
if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()