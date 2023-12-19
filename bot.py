from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import DiceEmoji

import os
from dotenv import load_dotenv
import random
load_dotenv()

TOKEN=os.getenv('TK')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print(update.to_json())
    await update.message.reply_dice(emoji=DiceEmoji.DICE,write_timeout=5000)
    # print(update.message.from_user.language_code)
    


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("dice", dice))


print("polling")
app.run_polling()