import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

QROQ_API_KEY = os.getenv("QROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the QROQ API URL and model
url = "https://api.groq.com/openai/v1/chat/completions"  # Assuming this is the correct QROQ API URL
model_name = 'llama-3.3-70b-versatile'  # Use the correct model from QROQ

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

class Reference:
    """
    A class to store previously fetched response from the QROQ API
    """
    def __init__(self) -> None:
        self.response = ""

# Instantiate Reference
reference = Reference()

# Function to clear the past conversation
def clear_past():
    """
    A function to clear the previous conversation and context.
    """
    reference.response = ""

@dispatcher.message_handler(commands=['clear'])
async def command_clear_handler(message: types.Message):
    """
    Handler for the '/clear' command to clear the conversation.
    """
    clear_past()
    await message.reply("Conversation cleared!")

@dispatcher.message_handler(commands=['start', 'help'])
async def command_start_help_handler(message: types.Message):
    """
    Handler for '/start' or '/help' commands to start the conversation and provide help.
    """
    help_command = """
    Hi there, I am your Telegram Bot powered by Monty! Please follow these commands:
    /start - Start the conversation.
    /help - To get this help menu.
    /clear - Clear the past conversation and context.
    I hope this helps! :)
    """
    await message.reply(help_command)

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    This handler processes user input and generates a response using the QROQ API.
    """
    print(f">>> User: \n\t{message.text}")

    try:
        # Send the user's message to the QROQ API
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {QROQ_API_KEY}"},
            json={
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message.text}
                ]
            }
        )

        # Check if the response is successful
        if response.status_code == 200:
            result = response.json()
            reference.response = result['choices'][0]['message']['content']
            print(f">>> Bot: \n\t{reference.response}")
            await bot.send_message(chat_id=message.from_user.id, text=reference.response)
        else:
            await message.reply(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error during API request: {str(e)}")
        await message.reply("Sorry, there was an error processing your request. Please try again later.")

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
