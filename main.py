import os
import logging

from dotenv import load_dotenv

import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()

tg_bot_token = os.environ['TG_BOT_TOKEN']
openai.api_key = os.environ['OPENAI_API_KEY']

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


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages.append({"role": "user", "context": update.message.text})
    completion = openai.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=messages)
    completion_answer = completion['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": completion_answer})

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=completion_answer)


if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler('start', start)
    chat_handler = CommandHandler('chat', chat)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()