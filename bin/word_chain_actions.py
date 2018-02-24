#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from collections import defaultdict
from google_speech import Speech
from google.assistant.library import Assistant

import random

def say(text, sox_effects=None):
    Speech(text, 'ja').play(sox_effects)

class WordChain:
    def __init__(self, assistant, words_file):
        self.assistant = assistant
        self.words = dict()
        self.dict = defaultdict(list)
        self.used_words = dict()

        self.load_words(words_file)

    def load_words(self, file):
        cnt = 0
        with open(file, 'r') as input:
            for line in input:
                word_tuple = line.strip().split(',')
                name = word_tuple[1]
                word_tuple.pop(1)
                self.words[name] = word_tuple
                self.dict[name[0]].append(name)
                cnt += 1
                #print(name, name[0], name[-1])
        print(len(self.words), cnt)

    def check(self, word):
        if word in self.used_words:
            return (False, '既に使ったのです。')
        
        if not word in self.words:
            return (False, 'ポケモンの名前ではありません。')
        if word[-1] == 'ん' or word[-1] == 'ン':
            return (False, 'ンが付いてます。')
        
        self.used_words[word] = self.words[word]
        del self.words[word]
        idx = 0
        list = self.dict[word[0]]
        for x in list:
            idx +=1 
            if x == word:
                del list[idx]
                break

        return (True, 'なかなかですね。')


    def pick_a_word(self, word):
        if len(self.words) == 0:
            return None

        candidate = self.dict[word[-1]]
        x = random.randint(0,len(candidate))
        pick = candidate[x]

        self.check(pick)

        return pick
        

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
