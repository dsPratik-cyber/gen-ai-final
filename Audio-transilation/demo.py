import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

openai_api_key = OPEN_API_KEY

audio_file = open("audiofile _name", 'rb')
output = openai.audio.translate('whisper-1', audio_file)
print(output)
