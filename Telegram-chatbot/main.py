import openai
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import sys

load_dotenv()
openai.api_key = os.getenv("OPEN_API_KEY")
TELEGRAM_BOT_TOKEN= os.getenv("TELEGRAM_BOT_TOKEN")


class Reference:
    """
    A Class to store previously response from the openai API
    """

    def __init__(self) ->None:
        self.response =""



reference = Reference()
model_name ='gpt-3.5-turbo'


# intialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

# for clearing the past conversation
def clear_past():
    """
    A function to clear the previous conversation and context.
    """
    reference.reference = ""


@dispatcher.message_handler(commands=['clear'])
async def command_clear_handler(message: types.Message):
    """
    This handler receives message with '/clear' command
    """
    clear_past()
    await message.reply("Conversation cleared!")




@dispatcher.message_handler(commands=['start','help'])
async def command_start_handler(message: types.Message):
    """"
    This handler receives message with '/start' or '/help'command"
    """
    await message.replay("hi\nI am Echo Bot!\nPowered by Monty.")

@dispatcher.message_handler(commands=['help'])
async def command_help_handler(message: types.Message):
    """
    This handler receives message with '/help' command
    """

    help_command = """
    Hi there , i'am Telegram bot created bt Monty! please follow these commands -
    /start - Start the conversation.
    /help - to get this help menu.
    /clear - Clear the past cobversation and context.
    I hope this helps. :)

    """
    
    await message.reply(help_command)

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    This handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> User: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": message.text}],
        logprobs=0
    )

    reference.response = response.choices[0].message['content']    
    print(f">>> Bot: \n\t{reference.response}")
    await bot.send_message(chat_id =message.from_user.id, text = reference.response)




if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates = True) # False for offlinr use