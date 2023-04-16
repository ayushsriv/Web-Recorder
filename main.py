#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import flash
import speech_recognition as sr

import os

fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
aib_move = ''

app = Flask(__name__)
app.jinja_env.autoescape = False

app.config['UPLOAD_FOLDER'] = '/Users/ayushsriv/Desktop/BOO/web-speech-recorder/source/recordings'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

import speech_recognition as sr
from IPython.display import display
import chess
import chess.engine
import time
import pyttsx3
import chess.svg
import asyncio

board = chess.Board()
r = sr.Recognizer()
mic = sr.Microphone()
engine = chess.engine.SimpleEngine.popen_uci(r"/Users/ayushsriv/Desktop/stockfish/12/bin/stockfish")

def spoken_to_algebraic(text):
    if text == 'kingside castle':
        return 'O-O'
    elif text == 'queenside castle':
        return 'O-O-O'
    # Define a dictionary that maps chess pieces to their spoken format
    piece_names = {'night': 'N', 'knight': 'N', 'bishop': 'B', 'rook': 'R', 'queen': 'Q', 'king': 'K'}
    action_words = {'takes': 'x', 'to': '', '2':''}
    algebraic = ''
    for t in text.split(" "):
        if t in piece_names:
            algebraic+=piece_names[t]
        elif t in action_words:
            algebraic+=action_words[t]
        else:
            algebraic+=t
        
    return algebraic


# Define a function that takes a chess move in algebraic notation and returns it in spoken format
def algebraic_to_spoken(move):    
    # Define a dictionary that maps chess pieces to their spoken format
    piece_names = {'P': 'pawn', 'N': 'knight', 'B': 'bishop', 'R': 'rook', 'Q': 'queen', 'K': 'king'}
    
    if move=='O-O':
        return "king side castle"
    elif move=='O-O-O':
        return "queen side castle" 
        
    # Construct the spoken format of the move
    spoken = ''
    for c in move:
        if c.isupper():
            spoken+=piece_names[c]
            spoken+=" "
        elif c=='x':
            spoken+="takes"
            spoken+=" "
        elif c=='+':
            spoken+="check"
        elif c=='#':
            spoken+="checkmate"        
        else:
            spoken+=c
    
    return spoken

@app.route("/speak", methods=['GET'])
def speak():
    global aib_move
    return {'aib_move': algebraic_to_spoken(aib_move)}

@app.route("/show", methods=['GET'])
def show():
    global fen
    return {'fen': fen}

@app.route("/move", methods=['POST'])
def move():
    global aib_move
    global fen
    try: 
        r = sr.Recognizer()
        file = request.files['audio_data']
        audio = sr.AudioFile(file)
        with audio as source:
            audio = r.record(source)
        move = r.recognize_google(audio)
        move = move.lower()
        print(move)
        if move == 'show board':
            display(board)
            # continue
        move = spoken_to_algebraic(move)
        board.parse_san(move)

        board.push_san(move)

        # AI moves second
        result = engine.play(board, chess.engine.Limit(time=0.1))
    
        # convert from uci to algebraic notation
        ai_move = chess.Move.from_uci(str(result.move))
        print(ai_move)
        aib_move = board.san(ai_move)

        board.push(result.move)
        fen = board.fen()

    except Exception as e:
        print(e)
        print("Not a valid move")
    
    return render_template('index.html', fen=fen, com_move=aib_move) 

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html', fen=fen, com_move=aib_move) 


if __name__ == "__main__":
    app.run()
