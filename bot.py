from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters
from telegram.constants import DiceEmoji
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv('TK')

import pymongo

try:
    print()
    client = pymongo.MongoClient("mongodb+srv://onlyplayxerath:iEEzRNyrBjaPPfTt@cluster0.00l13mt.mongodb.net/?retryWrites=true&w=majority")
    # select or create
    db = client["training-python"]
    collection= db["users"]
    print("connected to mongo")
except Exception as e:
    print(e)

def write_to_file(text:str):
    with open("log.txt",'a') as f:
        print(text,file=f)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    write_to_file(f"{update.effective_user.first_name} : {update.message.text}")
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print(update.to_json())
    write_to_file(f"{update.effective_user.first_name} : {update.message.text}")

    await update.message.reply_dice(emoji=DiceEmoji.DICE,write_timeout=5000)
    await update.message.reply_dice(emoji=DiceEmoji.BOWLING,write_timeout=5000)

    # print(update.message.from_user.language_code)
    
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    write_to_file(f"{update.effective_user.first_name} : {update.message.text}")

    text=update.message.text[4:]
    word_list = text.split()
    name=word_list[0]
    age=word_list[1]
    newuser={
        'name':name,
        'age':age,
    }
    
    await update.message.reply_text(f"new user added with id: {collection.insert_one(newuser).inserted_id}",
                                    reply_to_message_id=update.message.id,protect_content=True
                                    )

import re
def search_name_with_keyword(keyword):
    regex_pattern = re.compile(f'.*{re.escape(keyword)}.*', re.IGNORECASE)
    result = collection.find({'name': {'$regex': regex_pattern}})
    return list(result)


import json

async def message_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text=update.message.text
    datas = search_name_with_keyword(text)
    result=""
    for data in datas:
        result+=f"{data}\n"
        # result+=data['name']+ " - " + str(data['age'])+"\n"
    await update.message.reply_text(f"{result}"if result!="" else "Nothing was found")




app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("dice", dice))
app.add_handler(CommandHandler("add", add))
app.add_handler(MessageHandler(filters.TEXT, message_handle))

print("polling")
app.run_polling()