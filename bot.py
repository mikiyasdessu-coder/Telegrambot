import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# የ Gemini AI ሴቲንግ
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_URL = "https://telegrambot-0u7x.onrender.com"  # የ Render ዩአርኤልህ

app_flask = Flask(__name__)

# ቴሌግራም ቦት አፕሊኬሽን ማዋቀር
telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም Miki! እኔ የልቦናህ አጋር ጌሚኒ AI ነኝ፤ ምን ልረዳህ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("ይቅርታ፣ ከ Gemini ጋር ስንገናኝ ስህተት አጋጥሟል!")

# ሃንድለሮችን መጨመር
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app_flask.route('/')
def home():
    return "Bot is running with Webhook!"

@app_flask.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, telegram_app.bot)
    
    # ዩአርኤሉን በሂደት (Async) ማስኬድ
    import asyncio
    asyncio.run(telegram_app.process_update(update))
    return "OK", 200

if __name__ == '__main__':
    # ዌብሁክን ከቴሌግራም ጋር ማያያዝ
    import requests
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={RENDER_URL}/{TOKEN}")

    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
