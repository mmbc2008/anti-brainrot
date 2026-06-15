import os
from db import get_connection
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DB_URL = os.environ.get("DATABASE_URL")

bot = Bot(TOKEN)

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. get chat_id from update
    chat_id = update.effective_chat.id
    # 2. save to users table if not already there
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO users (chat_id) VALUES (%s)
                       ON CONFLICT (chat_id) DO NOTHING;""", (chat_id,))
    # 3. reply to the user
    await context.bot.send_message(chat_id, "Your account has been created.")
    
async def handle_notify(update, context):
    await send_new_events()
    
def format_event_text(event):
    return f"🎉 {event[1]}\n📍 {event[2]}\n📅 {event[3]} - {event[4]}\n💶 {event[6]}\n🔗 {event[7]}"
    
    

async def send_new_events():
    with get_connection() as conn:
        cursor = conn.cursor()
    # 1. for each user
        cursor.execute("SELECT chat_id FROM users;")
        users = cursor.fetchall()
        
    #2 For each unseen event
        for user in users:
            with get_connection() as conn:
                cursor = conn.cursor()
                # 3 Select all event details for the message 
                cursor.execute("SELECT * FROM events WHERE id NOT IN (SELECT event_id FROM notifications WHERE chat_id = %s);", (user[0],))
                events = cursor.fetchall()
                for event in events:
                    text = format_event_text(event)
                    await bot.send_message(user[0], text)
                    # 4. Insert this into notifications
                    cursor.execute("INSERT INTO notifications (event_id, chat_id) VALUES (%s, %s);", (event[0], user[0]))
                
    

                


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("notify", handle_notify))
    app.add_handler(CommandHandler("start", handle_start))
    app.run_polling()