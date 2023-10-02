import time
import threading
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from selenium import webdriver

# Replace 'YOUR_API_TOKEN' with your actual Telegram bot API token
TOKEN = '6545788125:AAFscNRGesAI3ZY9b81VaRA7JkY5SDc06Z4'
ACTIVE_CHAT_ID = None
URL_TO_REFRESH = "https://tame-red-sturgeon-gown.cyclic.cloud/"

# Function to handle the /start command
# (Keep this function as it is from the original bot code)
# ... [Rest of the Telegram bot code] ...

# Function to handle incoming messages
# (Keep this function as it is from the original bot code)
# ... [Rest of the Telegram bot code] ...

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

# Simulate activity every 5 minutes to keep the bot running
def simulate_activity(context: CallbackContext) -> None:
    global ACTIVE_CHAT_ID
    if ACTIVE_CHAT_ID:
        # Check if there are new messages to reply to
        # This is not efficient, but it's a workaround for the limitation of Cyclic
        messages = context.bot.get_updates()
        if messages:
            for message in messages:
                if message.message:
                    update = Update.de_json(message.to_dict(), context.bot)
                    on_message(update, None)

        # Send periodic "Bot is active" message
        context.bot.send_message(ACTIVE_CHAT_ID, text='Bot is active!')

    threading.Timer(300, simulate_activity, args=[context]).start()

# Function to open and refresh the URL using Selenium
def refresh_url():
    # Initialize the web driver (you may need to specify the path to your browser driver)
    driver = webdriver.Chrome()
    
    try:
        # Open the URL
        driver.get(URL_TO_REFRESH)
    
        # Refresh the page every 5 minutes
        while True:
            time.sleep(300)  # Wait for 5 minutes
            driver.refresh()  # Refresh the page
    
    except KeyboardInterrupt:
        # Close the browser when interrupted
        driver.quit()

def main():
    global updater
    global ACTIVE_CHAT_ID

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Add handlers for new members and leaving members
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_members))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_member))

    # Add other handlers
    # (Keep this section as it is from the original bot code)
    # ... [Rest of the handlers] ...

    # Start the Bot
    updater.start_polling()

    # Start simulating activity every 5 minutes
    simulate_activity(dp)

    # Start refreshing the URL
    refresh_url()

    updater.idle()

if __name__ == '__main__':
    main()
