import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, jsonify ,render_template

load_dotenv()
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

openai_api_key = OPEN_API_KEY

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"

@app.route("/", methoda = ='GET', 'POST')
def main():
    if request.method == 'POST':
        language = request.form['language']
        file = request.files["files"]
        if file:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            audia_file = open("static/" + filename, "rb")
            transcript = openai.audio.translate('whisper-1', audia_file)

            response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages = [{ "role": "system", "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}" }, 
                                { "role": "user", "content": transcript.text }],
                    temperature=0,
                    max_tokens=256
                  )
            
            return jsonify(response)             
        
    return render_template('index.html')
                                                

