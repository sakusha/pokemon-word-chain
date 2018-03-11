#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from google.assistant.library import Assistant
from google_speech import Speech
from word_chain import WordChain

import time

def say(text, sox_effects=None):
    Speech(text, 'ja').play(sox_effects)
    time.sleep( .5 )

game = None

def my_actions(assistant, event, device_id):
    '''
    Entry point for the word chain game
    '''
    text = event.args['text'].lower()
    print(text)

    global game

    if 'ポケモンしりとり' in text:
        assistant.stop_conversation()
        if game:
            say('既にゲームは始まってますよ。')
            return

        game = WordChain('pokemon-name.txt')
        say('じゃあ、私から始めます。')

        pick = game.pick_a_word()
        say(pick)
        result=game.check(pick)
        if not result[0]:
            game = None
            say(result[1]+'貴方の勝ちです。おめでとうございます！')
            return

        say('では、貴方のターンです。')

    elif 'ポケモンの名前' in text:
        assistant.stop_conversation()
        read_pokemon()

    elif '私のターン' in text:
        assistant.stop_conversation()
        words = text.strip().split(' ')

        if not '私のターン' in words[0]:
            say('どういう事ですか？')
            return

        if not game:
            say('ゲームは始まってませんよ。')
            return

        #pokemon_tuple = text.strip().split(' ')
        if len(words) <= 1:
            game = None
            say('何も言ってないです。それじゃ～、私の勝ちです。うははは。')
            return

        print(words[1])
        say(words[1]+'ですね。')

        '''
                 speaker's turn
        '''
        result=game.check(words[1])
        if not result[0]:
            game = None
            say(result[1]+'それじゃ～、私の勝ちです。うははは。')
            return

        say(result[1]+'では、私のターンです。')

        word = game.pick_a_word(words[1])

        say(word)

        result=game.check(word)
        if not result[0]:
            game = None
            say(result[1]+'貴方の勝ちです。おめでとうございます！')
            return

        say('では、貴方のターンです。')
