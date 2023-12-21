from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import DiceEmoji
import os
from dotenv import load_dotenv
import random
load_dotenv()
TOKEN=os.getenv('TK')

import pymongo

try:
    print()
    client = pymongo.MongoClient("mongodb+srv://onlyplayxerath:iEEzRNyrBjaPPfTt@cluster0.00l13mt.mongodb.net/?retryWrites=true&w=majority")
    # select or create
    db = client["training-python"]
    collection= db["users"]
    user={
        "name":"Tan",
        "age":30,
    }
    print(f"new user added with id: {collection.insert_one(user).inserted_id}")
    print("connected to mongo")
except Exception as e:
    print(e)





async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print(update.to_json())
    await update.message.reply_dice(emoji=DiceEmoji.DICE,write_timeout=5000)
    await update.message.reply_dice(emoji=DiceEmoji.BOWLING,write_timeout=5000)

    # print(update.message.from_user.language_code)
    


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("dice", dice))


print("polling")
app.run_polling()