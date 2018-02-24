#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from collections import defaultdict
from google_speech import Speech
from google.assistant.library import Assistant

import random

def say(text, sox_effects=None):
    Speech(text, 'ja').play(sox_effects)

def my_actions(assistant, event, device_id):
    text = event.args['text'].lower()
    print(text)

    if 'ポケモンしりとり' in text:
        assistant.stop_conversation()
        print(text+' start')
    elif 'ポケモンの名前' in text:
        assistant.stop_conversation()
        print(text+' start')
        read_pokemon()
    elif '私のターン' in text:
        assistant.stop_conversation()
        pokemon_tuple = text.strip().split(' ')
        if len(pokemon_tuple) > 1:
            print(pokemon_tuple[1])
            say(pokemon_tuple[1]+'ですね。')
        else:
            say('私の勝ちです。うははは。')

def read_pokemon():
    word_chain = WordChain( None, '../data/pokemon-name.txt')
    
    with open(file, 'r') as input:
        for line in input:
            word_tuple = line.strip().split(',')
            name = word_tuple[1]
            #word_tuple.pop(1)
            cnt += 1
            #print(name, name[0], name[-1])
        print(len(self.words), cnt)

if __name__ == '__main__':
    read_pokemon()
