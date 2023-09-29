from typing import Final
from telegram import Update
import requests
from User import User
from File import File
from inst import *
import time
import schedule
from datetime import datetime, time as dt_time
import asyncio
import multiprocessing


from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Telegram Token
TOKEN: Final = "6443425010:AAG_qpNzH4P36W1g2tHrLu9AtgjuWXopJnM"
# Telegram Bot username
BOT_USERNAME = "@cntic_social_media_bot"
# List to store it your username and password
Credantiels = [None] * 2
# Post option  1=>for story 2=>for post  -1=>default
# option = -1


# To start the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello ! Thanks for chatting with me! I am CNTIC bot"
    )


# Get bot commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " I am CNTIC bot Please type something so i can respond\n  /instg :instgram options \n /about:to know more about this bot "
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "CNTIC_social_media_bot  is social media boot developed by Soheib Benchabana this bot can use it to post on Instagram automatically and chat with people "
    )


# custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" This is custom command")


# instgram options
async def instg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " To post remotly by chosing between to modes \n /poststory (to post a story you should create an account to get this functionality) \n /postapost (to post a post you should create an account to get this functionality) \n/createAccount (crate you account you should create an account to get this functionality) \n /deleteInstgAccount (to delete your account from my database)"
    )


# delete your instgram account registred in bot database
async def deleteInstgAccount_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    telegram_user_id = update.message.from_user.id
    result = delete_user_account(telegram_user_id)
    if result:
        await update.message.reply_text("user account and files deleted successfully")
    else:
        await update.message.reply_text("error to deleting this user account")


# use it to set you file option as story


async def poststory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resp = 'you can do this by sending a picture and you should specify time and post option in caption section folowing this example(time=year-month-day hour:minute,option=1 )"'

    await update.message.reply_text(resp)


async def postapost_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_test = User()
    if user_test.get_user_by_id(update.message.from_user.id):
        # global option
        # option = 2
        resp = 'you can do this by sending a picture and you should specify time and post option in caption section following this example(time:year-month-day hour:minute,option=2)"'
    else:
        resp = "you should create account first by using /createAccount command "

    await update.message.reply_text(resp)


# use it to create new account using your instgram credentials
async def createAccount_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resp = "enter instgram username and password to get our shedule posting services ,\n you should writed likethe following example (username:<your_username>,password:<password>)"
    await update.message.reply_text(resp)


# Responses


def handle_response(text: str) -> str:
    processed: str = text

    if "hello" in processed:
        return "Hey there"
    if "social media" in processed:
        return "facebook:https://www.facebook.com/profile.php?id=100086918944526 \n instagram:https://instagram.com/cntic_club?igshid=YmMyMTA2M2Y=\ndiscord:https://discord.com/invite/8Fb7bAYp\n CNTIC website:https://cntic-club.com/"
    if "what is cntic" in processed:
        return "cntic, short for the Club des Nouvelles Technologies d'Information et de Communication, is a dynamic organization dedicated to the realm of cutting-edge information technology (IT) and communication. Our mission revolves around facilitating an enlightening journey into the world of new technologies. Through meticulously organized courses, conferences, and challenges, we empower individuals to acquaint themselves with the latest IT trends and chart a course toward their aspirations."
    if "what is your activities" in processed:
        return "1/👨‍💻 Tech Enthusiasm\n2/🔧 Practical Learning\n3/🌐 Networking\n4/🌟 Resource Hub\n5/🚀 Guest Speakers\n6/🌆 Career Advancement"
    if "your name" in processed:
        return "I'm cntic bot."
    if "how are you" in processed:
        return "I am good"
    if "tell me a joke" in processed:
        return (
            "Why did the computer catch a cold? Because it had too many windows open!"
        )
    if "can do" in processed:
        return "I can post on Instagram automatically with correct scheduling time and chat with people you can check my options using /help command"
    if "I love cntic club" in processed:
        return "Remember to subscribe"
    if "facebook" in processed:
        return "https://www.facebook.com/profile.php?id=100086918944526"
    if "instagram" in processed:
        return "https://instagram.com/cntic_club?igshid=YmMyMTA2M2Y="
    if "linkedin" in processed:
        return "https://www.linkedin.com/company/cntic-club/"
    if "discord" in processed:
        return "https://discord.com/invite/8Fb7bAYp"
    if "website link" in processed:
        return "https://cntic-club.com/"
    if "thank you" in processed:
        return "your welcome"
    if "join to your club" in processed:
        return "You can join our club by signing up on the CNTIC registration form at this link: https://cntic-club.com/registration/"
    return "I'm not sure I understand. Please ask another question."


# Messages
# Corrected variable name to 'response' throughout the code
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    # resp = ""
    print(f'User ({update.message.chat.id}) in  type {message_type}: "{text}"')

    if message_type == "supergroup" or message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)

            if "username:" in text or "password:" in text:
                telegram_id = update.message.from_user.id
                user = User(telegram_id)
                if user.process_input(text):
                    return await update.message.reply_text(
                        "Account created successfuly"
                    )
                else:
                    return await update.message.reply_text(
                        "can not  create this account "
                    )
            else:
                return await update.message.reply_text(response)
        else:
            return
    else:
        if "username:" in text and "password:" in text:
            telegram_id = update.message.from_user.id
            user = User(telegram_id)
            if user.process_input(text):
                response = "Account created successfuly"
            else:
                response = "We can not create this account"
        else:
            response: str = handle_response(text)
        print("-----------------current responce------------", response)
        return await update.message.reply_text(response)


# Handle  with sent images
async def handle_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.photo:
        photo = message.photo[-1]
        # file_id = photo.file_id
    # Check if there is also a text message
    if message.caption:
        captions = handle_caption(message.caption)
        print("captions:", captions)
        if captions:
            option = captions[0]
            time_message = captions[1]
            print("time:", time_message)
            # Extract sent time from the text message if it contains a time
            sent_time = extract_sent_time(time_message)

    # Access the file URL of the photo (assuming it's available)
    try:
        photo_file = await photo.get_file()
        file_url = photo_file.file_path  # Obtain the file URL
        print("-------------option------------", option)
        # Download the file from the URL
        response = requests.get(file_url)
        if response.status_code == 200:
            file_data = response.content
            timestamp = int(time.time() * 1000)
            telegram_id = update.message.from_user.id
            id = f"{telegram_id}_{timestamp}"

            file = File(id, file_data, sent_time, option, telegram_id)
            created_file = file.create_file()
            if created_file == True:
                print("----finsh dowonload file opration----")
                resp = "the story successfuly stored and will post it"
            else:
                resp = f"user with {telegram_id} deos not exited you should create new user account "

            await update.message.reply_text(resp)

        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except Exception as e:
        # Handle exceptions, e.g., log the error
        print(f"An error occurred: {e}")


def handle_caption(caption: str):
    arr = [None] * 2
    try:
        captions = caption.split(",")
        for cap in captions:
            key, value = cap.split("=")
            if key == "option":
                arr[0] = value
            elif key == "time":
                arr[1] = value
        return arr
    except Exception as e:
        print("invailid input")
        return []


def extract_sent_time(text_message: str):
    # You'll need to implement a logic to extract the sent time from the text message
    # For example, you can search for a specific time format in the message
    # and parse it into a datetime object
    # Here's a basic example assuming the time is in "HH:MM" format:
    try:
        time_str = text_message.strip()
        sent_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        return sent_time
    except ValueError:
        return None  # Invalid or no time found


# delete user account using user id
def delete_user_account(id):
    user_del = User()
    user_files = File()
    res1 = user_del.delete_user_by_id(id)
    res2 = user_files.delete_All_files(id)
    return 1 if res1 == True else False


# check schedule for posting every time
def check_and_post_scheduled_content():
    print("inside scheduled...")
    user_manager = User()
    file_manager = File()
    users = user_manager.get_all_users()
    print(users)
    for user_data in users:
        print("user data:", user_data)
        user_id = user_data[0]  # user id
        credentials = [user_data[1], user_data[2]]  # username and password
        files = file_manager.get_user_files(user_id)  # get all user files
        for file in files:
            file_id = file[0]
            print("time:", file[2])
            isposted = file[4]  # file status
            posting_time = datetime.strptime(
                file[2], "%Y-%m-%d %H:%M:%S"
            )  # 2023-09-28 10:19 (time format)
            print(posting_time)

            if check_post_time(posting_time) and checkPostStatus(isposted) == 1:
                print("yes this is time of posting....")
                file_status = file_manager.changePostType(
                    file_id
                )  # changing the post type
                print("file status=", file_status)
                result = post_file(file, credentials)  # posting a file
                if result != -1:
                    print("The post was successfully posted...")
                else:
                    print("Error posting file with ID", file[0])
            elif check_post_time(posting_time):  # ccheck posting time
                print(f"The file with id {file_id} was posted before....")

    # close connection with database
    file_manager.disconnect_file()
    user_manager.disconnect_user()


# Check the post time
def check_post_time(posting_time):
    return datetime.now() >= posting_time


# check post status if was posted or no
def checkPostStatus(isposted):
    print(isposted)
    if isposted:
        return 0
    else:
        return 1


# Function to post a file (implement sendStory and sendPost as needed)
def post_file(file, credentials):
    if int(file[3]) == 1:
        return sendStory(credentials, file[1])
    elif int(file[3]) == 2:
        return sendPost(credentials, file[1])
    else:
        return -1


# check errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# bot function


def initialize_bot(user_lock=None, file_lock=None):
    if user_lock:
        with user_lock:
            print("Starting bot")
            app = Application.builder().token(TOKEN).build()

            # Commands
            app.add_handler(CommandHandler("start", start_command))
            app.add_handler(CommandHandler("help", help_command))
            app.add_handler(CommandHandler("about", about_command))
            app.add_handler(CommandHandler("custom", custom_command))
            app.add_handler(CommandHandler("instg", instg_command))
            app.add_handler(CommandHandler("poststory", poststory_command))
            app.add_handler(CommandHandler("postapost", postapost_command))
            app.add_handler(
                CommandHandler("deleteInstgAccount", deleteInstgAccount_command)
            )
            app.add_handler(CommandHandler("createAccount", createAccount_command))

            # Messages
            app.add_handler(MessageHandler(filters.TEXT, handle_message))
            app.add_handler(MessageHandler(filters.PHOTO, handle_picture))

            # Errors=
            app.add_error_handler(error)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Poll the bot
            print("Polling..")

            # check telegram bot server every three secands
            app.run_polling(poll_interval=3)


# schedul files check file posting operation every time
def scheduled_content(user_lock=None, file_lock=None):
    if file_lock:
        with file_lock:
            schedule.every(3).seconds.do(check_and_post_scheduled_content)
            while True:
                schedule.run_pending()
                time.sleep(3)  # Adjust the interval as needed


def main():
    # Create Lock for synch between processes
    user_lock = multiprocessing.Lock()
    file_lock = multiprocessing.Lock()

    # Create two separate processes, one for initialize_bot and one for scheduled_content
    bot_process = multiprocessing.Process(
        target=initialize_bot, args=(user_lock, file_lock)
    )
    scheduled_process = multiprocessing.Process(
        target=scheduled_content, args=(user_lock, file_lock)
    )

    # Start both processes
    bot_process.start()
    scheduled_process.start()

    # Wait for both processes to complete before continuing
    bot_process.join()
    scheduled_process.join()


if __name__ == "__main__":
    main()
