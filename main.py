#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import flash
import speech_recognition as sr

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/ayushsriv/Desktop/BOO/web-speech-recorder/source/recordings'

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        print("hello")
        r = sr.Recognizer()
        file = request.files['audio_data']
        print(file)
        audio = sr.AudioFile(file)
        with audio as source:
            audio = r.record(source)
        print(r.recognize_google(audio))

        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()
