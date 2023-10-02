from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_API_TOKEN' with your actual Telegram bot API token
TOKEN = '6545788125:AAFscNRGesAI3ZY9b81VaRA7JkY5SDc06Z4'

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Physics Wallha Telegram channel!')

# Function to handle new members joining the channel
def new_chat_members(update: Update, context: CallbackContext) -> None:
    for member in update.message.new_chat_members:
        update.message.reply_text(f'Welcome to Physics Wallha Telegram channel, {member.first_name}!')

# Function to handle members leaving the channel
def left_chat_member(update: Update, context: CallbackContext) -> None:
    left_member = update.message.left_chat_member
    update.message.reply_text(f'{left_member.first_name} has left the Physics Wallha Telegram channel.')

# Function to send a welcome message to all existing members
def send_welcome_to_existing_members(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    members_count = context.bot.get_chat_members_count(chat_id)
    update.message.reply_text(f'Welcome to Physics Wallha Telegram channel! We currently have {members_count} members.')

# Simulate activity every 5 minutes to keep the bot running
def simulate_activity(context: CallbackContext) -> None:
    context.bot.send_message(context.job.context, text='Bot is active.')

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_members))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_member))
    dp.add_handler(CommandHandler("welcome_existing_members", send_welcome_to_existing_members))

    # Start the Bot
    updater.start_polling()

    # Schedule the activity simulation every 5 minutes
    updater.job_queue.run_repeating(simulate_activity, interval=300, context=updater.bot.get_updates()[-1].message.chat_id)

    updater.idle()

if __name__ == '__main__':
    main()
