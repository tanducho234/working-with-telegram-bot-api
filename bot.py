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


import requests
ACCESS_KEY="aMv_Q4oxdTHal72lS32lF4FOWmq6ZwVr0bu7LLh7OSw"
API_ADDRESS_RANDOM=f'https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}'

async def random_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response=requests.get(API_ADDRESS_RANDOM)
    if response.status_code==200:
        image_url=response.json().get('urls',{}).get('regular')
        await update.message.reply_photo(photo="image_url",caption="Random Image from Unsplash")
    else:
        await update.message.reply_text("Something went wrong")

API_ADDRESS_SEARCH=f'https://api.unsplash.com/search/photos?client_id={ACCESS_KEY}&query='

async def search_images(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response=requests.get(API_ADDRESS_SEARCH)
    keyword=update.message.text[14:]
    print(keyword)
    if not keyword:
        await update.message.reply_text("Please enter a keyword")
        return
    else:
        response=requests.get(API_ADDRESS_SEARCH+keyword)
        if response.status_code==200:
            search_results=response.json().get('results')[:4]
            for photo_info in search_results:
                image_url=photo_info.get('urls',{}).get('regular')
                await update.message.reply_photo(photo=image_url)
            # result=""
            # for image in images:
            #     result+=f"{image['urls']['regular']}\n"
            # await update.message.reply_text(result)
        else:
            await update.message.reply_text("Something went wrong")



import requests
from bs4 import BeautifulSoup    
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url="https://znews.vn/"
    response=requests.get(url)
    soup=BeautifulSoup(response.content,"html.parser")
    for i in range(1,8):
        element=soup.select_one(f"article:nth-child({i}) > header > p.article-title > a")
        image_url=soup.select_one(f"#section-latest > section > div > article:nth-child({i}) > p > a > img").get("data-src")
        caption=element.text
        tempoUrl=element.get("href")
        tempoResponse=requests.get(tempoUrl)
        tempoSoup=BeautifulSoup(tempoResponse.content,"html.parser")

        date=tempoSoup.select_one("li.the-article-publish").text
        await update.message.reply_photo(photo=image_url,caption=caption+"\n"+date)



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("dice", dice))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("randomimage", random_image))
app.add_handler(CommandHandler("searchimages", search_images))
app.add_handler(CommandHandler("news", news))



app.add_handler(MessageHandler(filters.TEXT, message_handle))

print("polling")
app.run_polling()