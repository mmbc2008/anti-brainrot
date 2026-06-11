import os
import sqlite3
from db import get_connection
from dotenv import load_dotenv
from pathlib import Path
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DB_PATH = Path(__file__).parent / "data" / "bot.db"

bot = Bot(TOKEN)

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. get chat_id from update
    chat_id = update.effective_chat.id
    # 2. save to users table if not already there
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?);", (chat_id,))
    # 3. reply to the user
    await context.bot.send_message(chat_id, "Your account has been created.")
    
async def handle_notify(update, context):
    await send_new_events()
    
def format_event_text(event):
    return f"🎉 {event[1]}\n📍 {event[2]}\n📅 {event[3]} - {event[4]}\n💶 {event[6]}\n🔗 {event[7]}"
    
    

async def send_new_events():
    # 1. query events WHERE notified = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE notified=0;")
        events = cursor.fetchall()
    # 2. for each event, send to all users
        cursor.execute("SELECT chat_id FROM users;")
        users = cursor.fetchall()
    for event in events:
        with get_connection() as conn:
            cursor = conn.cursor()
            for user in users:
                print(event)
                text = format_event_text(event)
                await bot.send_message(user[0], text)
                # 3. mark notified = 1
            cursor.execute("UPDATE events SET notified=1 WHERE id=?;", (event[0],))


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("notify", handle_notify))
    app.add_handler(CommandHandler("start", handle_start))
    app.run_polling()