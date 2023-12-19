from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN=os.getenv('TK')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token("6900470673:AAFM2vEso8_ac323E-jAEFbVz_zJUoAupD8").build()

app.add_handler(CommandHandler("hello", hello))

print("polling")
app.run_polling()