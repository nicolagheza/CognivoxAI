import os
import telebot
from dotenv import load_dotenv
from groq import Groq
import tempfile
from pathlib import Path

from telebot.apihelper import ApiTelegramException

from GraphManager import GraphManager
from utils import Utils

load_dotenv()

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")
Utils.set_env("LANGCHAIN_TRACING_V2")
Utils.set_env("LANGCHAIN_API_KEY")
Utils.set_env("LANGCHAIN_ENDPOINT")
Utils.set_env("LANGCHAIN_PROJECT")
Utils.set_env("TOGETHER_API_KEY")


def is_subscribed(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False


def reply(message):
    graph = GraphManager().create_graph()
    config = {"configurable": {"thread_id": message.chat.id}}
    response = graph.invoke({"messages": [("user", message.text)]}, config)
    bot.send_message(message.chat.id, response["messages"][-1].content)


def check_subscription(message):
    if not is_subscribed(TELEGRAM_CHANNEL_ID, message.from_user.id):
        bot.reply_to(message, "Please subscribe to our channel to use this bot @nicode_solutions")
        return False
    return True


# Telegram Bot
bot = telebot.TeleBot(TELEGRAM_API_KEY)

client = Groq(api_key=GROQ_API_KEY)


@bot.message_handler(commands=['start', 'help'])
def start_help_message(message):
    if check_subscription(message):
        bot.reply_to(message, 'Hello I am Cognivox AI. A friendly bot created by nicode.solutions')


@bot.message_handler(commands=['clearcontext'])
def clear_context_message(message):
    if check_subscription(message):
        bot.reply_to(message, '🗑 Context has been cleaned.️')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    if not check_subscription(message):
        return

    try:
        # Get file info and download
        file_info = bot.get_file(message.voice.file_id)
        voice_content = bot.download_file(file_info.file_path)

        # Use a temporary file
        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
            temp_file.write(voice_content)
            temp_file_path = temp_file.name

        # Process the audio file
        with open(temp_file_path, "rb") as audio_file:
            translation = client.audio.translations.create(
                file=(Path(temp_file_path).name, audio_file),
                model="whisper-large-v3",
                prompt="You can translate both English and Italian",
                response_format="json",
                temperature=0.0
            )

        # Clean up the temporary file
        os.unlink(temp_file_path)

        # Process the translation
        if translation and hasattr(translation, 'text'):
            message.text = translation.text
            reply(message)
        else:
            bot.reply_to(message, "Sorry, I couldn't process the voice message. Please try again.")

    except Exception as e:
        bot.reply_to(message, f"An error occurred while processing your voice message: {str(e)}")
        # Log the error for debugging
        print(f"Error in voice processing: {str(e)}")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def text_processing(message):
    if check_subscription(message):
        reply(message)


bot.infinity_polling()
