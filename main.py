from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import threading

# Replace 'YOUR_API_TOKEN' with your actual Telegram bot API token
TOKEN = '6545788125:AAFscNRGesAI3ZY9b81VaRA7JkY5SDc06Z4'
ACTIVE_CHAT_ID = None

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Physics Wallha Telegram channel!')

# Function to handle new members joining the channel
def new_chat_members(update: Update, context: CallbackContext) -> None:
    global ACTIVE_CHAT_ID
    for member in update.message.new_chat_members:
        update.message.reply_text(f'Welcome to Physics Wallha Telegram channel, {member.first_name}!')
    ACTIVE_CHAT_ID = update.message.chat_id

# Function to handle members leaving the channel
def left_chat_member(update: Update, context: CallbackContext) -> None:
    left_member = update.message.left_chat_member
    update.message.reply_text(f'{left_member.first_name} has left the Physics Wallha Telegram channel.')

# Function to send a welcome message to all existing members
def send_welcome_to_existing_members(update: Update, context: CallbackContext) -> None:
    global ACTIVE_CHAT_ID
    chat_id = update.message.chat_id
    members_count = context.bot.get_chat_members_count(chat_id)
    update.message.reply_text(f'Welcome to Physics Wallha Telegram channel! We currently have {members_count} members.')
    ACTIVE_CHAT_ID = chat_id

# Simulate activity every 5 minutes to keep the bot running
def simulate_activity():
    global ACTIVE_CHAT_ID
    if ACTIVE_CHAT_ID:
        # Check if there are new messages to reply to
        messages = updater.bot.get_updates()
        for message in messages:
            if message.message:
                update = Update.de_json(message.to_dict(), updater.bot)
                on_message(update, None)

        # Send periodic "Bot is active" message
        updater.bot.send_message(ACTIVE_CHAT_ID, text='Bot is active!')

    threading.Timer(300, simulate_activity).start()

# Function to handle incoming messages
def on_message(update: Update, context: CallbackContext) -> None:
    message: Message = update.message
    chat_id = message.chat_id
    text = message.text

    # Reply to the received message
    if text:
        message.reply_text(f"You said: {text}")

def main():
    global updater
    global ACTIVE_CHAT_ID

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_members))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_member))
    dp.add_handler(CommandHandler("welcome_existing_members", send_welcome_to_existing_members))
    dp.add_handler(MessageHandler(Filters.text, on_message))

    # Start the Bot
    updater.start_polling()

    # Start simulating activity every 5 minutes
    simulate_activity()

    updater.idle()

if __name__ == '__main__':
    main()
