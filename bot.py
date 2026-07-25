import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም Miki! እኔ የልቦናህ አጋር ጌሚኒ AI ነኝ፤ ምን ልረዳህ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = model.generate_content(update.message.text)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
