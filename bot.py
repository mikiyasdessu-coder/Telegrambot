import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 1. ሬንደር ፖርት እንዲያገኝ ትንሽ የልብ ምት (Dummy) ሰርቨር መፍጠር
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# 2. የ Gemini AI ሴቲንግ
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም Miki! እኔ የልቦናህ አጋር ጌሚኒ AI ነኝ፤ ምን ልረዳህ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = model.generate_content(update.message.text)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    # ፍላስክን ከበስተጀርባ በሌላ ቲሬድ (Thread) ማስጀመር
    t = threading.Thread(target=run_flask)
    t.start()

    # ቴሌግራም ቦቱን ማስጀመር
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
