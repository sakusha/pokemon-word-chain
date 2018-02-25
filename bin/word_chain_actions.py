#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from collections import defaultdict
from google_speech import Speech
from google.assistant.library import Assistant

import random
import re
import sys

def say(text, sox_effects=None):
    Speech(text, 'ja').play(sox_effects)

class WordChain:
    def __init__(self, assistant, words_file):
        self.assistant = assistant

        self.jap_base = dict()
        self.jap_comb = dict()

        self.words = dict()
        self.dict = defaultdict(list)
        self.used_words = dict()
        self.expected_char=None

        self._load_gojuon()
        self._load_combination()

        self._load_words(words_file)

    def _load_gojuon(self):
        with open('../data/gojuon.txt', 'r') as input:
            for line in input:
                chars = line.strip().split(',')
                base = chars[0]
                chars.pop(0)
                for char in chars:
                    self.jap_base[char]=base

    def _load_combination(self):
        with open('../data/combination.txt', 'r') as input:
            for line in input:
                chars = line.strip().split(',')
                self.jap_comb[chars[0]]=chars[1]

    def _load_words(self, file):
        cnt = 0
        ptn = re.compile(r"([・：]|\(.*?\))")
        with open(file, 'r') as input:
            for line in input:
                word_tuple = line.strip().split(',')
                name = word_tuple[1]
                word_tuple.pop(1)
                name = ptn.sub('', name).strip()
                self.words[name] = word_tuple
                self.dict[name[0]].append(name)
                cnt += 1
                print(name, name[0], name[-1])
        print(len(self.words), cnt)

    def get_last_char(self, word):
        last = word[-1]
        if last == 'ー':
            last = self.jap_base[word[-2]]

        if last in self.jap_comb:
            last=self.jap_comb[last]

        return last

    def check(self, word):
        if not word:
            return(False, 'もう使える物がないですね。')

        if self.expected_char:
            print('current=('+self.expected_char+')')
        else:
            print('current=()')

        if self.expected_char and word[0] != self.expected_char:
            return (False, '正しくないです。')
        
        if word in self.used_words:
            return (False, '既に使ったのですよ。')
        
        if not word in self.words:
            return (False, 'ポケモンの名前ではありません。')
        if word[-1] == 'ん' or word[-1] == 'ン':
            return (False, 'ンが付いてます。')
        
        self.used_words[word] = self.words[word]
        del self.words[word]
        idx = 0
        list = self.dict[word[0]]
        for x in list:
            if x == word:
                del list[idx]
                break
            idx +=1 

        self.expected_char=self.get_last_char(word)
        print('new=('+self.expected_char+')')

        return (True, 'なかなかですね。')

    def pick_a_word(self, word):
        if len(self.words) == 0:
            return None

        last = self.get_last_char(word)

        candidate = self.dict[last]
        if len(candidate) == 0:
            return None

        x = random.randint(0,len(candidate))
        pick = candidate[x]

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

def test_pokemon():
    word_chain = WordChain( None, '../data/pokemon-name.txt')
    
    test_word = input('Enter pokemon name: ')
    
    inGame = True
    while inGame:
        result = word_chain.check(test_word)

        if not result[0]:
            inGame = result[0]
            print(result[1])    
            continue

        print(result)

        word = word_chain.pick_a_word(test_word)

        print(word)
        result=word_chain.check(word)
        if not result[0]:
            inGame = result[0]
            print(result[1])    
            continue

        test_word = input('Enter pokemon name: ')
        if not test_word:
            inGame = False

if __name__ == '__main__':
    test_pokemon()
