from flask import Flask, render_template, request, redirect, url_for
from flask import session
from uuid import uuid4

import requests


app = Flask(__name__)


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer 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"}

from flask import Flask, render_template, request, jsonify, json
from werkzeug.utils import secure_filename



@app.route('/')
def index():
    return render_template('index.html')




@app.route('/result', methods=['POST'])
def result():
    audio = request.files['audio']  # Audio faylni olish
    uuid = str(uuid4())
    audio.save('audios/audio{}.wav'.format(uuid))  # Audio faylni saqlash
    filename ='audios/audio{}.wav'.format(uuid)  # Audio faylni tayyorlaymiz
    response = query(filename)  # Huggingface API ga so'rov jo'natamiz
    return response['text']

@app.route('/stt', methods=['GET', 'POST'])
def stt():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save('files/' + filename)
        response = query('files/' + filename)
        return response['text']
        



def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)