import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging ማስተካከያ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start ሲባል የሚሰጠው ምላሽ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! ቦቱ በትክክል እየሰራ ነው! 🚀")

if __name__ == '__main__':
    # የቴሌግራም ቦት Token ህን እዚህ ቦታ ላይ በግልጽ አስገባ (ወይም Environment Variable ተጠቀም)
    TOKEN = "8591437134:AAFQyyHHNzCTE1xFOY8xyzkXMDTxHviDOOM"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()
