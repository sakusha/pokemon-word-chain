#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from collections import defaultdict
from google_speech import Speech
from google.assistant.library import Assistant

import random
import re
import sys
import time

def say(text, sox_effects=None):
    Speech(text, 'ja').play(sox_effects)
    time.sleep( .5 )

'''
    Word chain game
'''
class WordChain:
    '''
        builds words dictionary and required files
    '''
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

    '''
        load mappings for the long sound
    '''
    def _load_gojuon(self):
        with open('../data/gojuon.txt', 'r') as input:
            for line in input:
                chars = line.strip().split(',')
                base = chars[0]
                chars.pop(0)
                for char in chars:
                    self.jap_base[char]=base

    '''
        load mappings for small katakana
    '''
    def _load_combination(self):
        with open('../data/combination.txt', 'r') as input:
            for line in input:
                chars = line.strip().split(',')
                self.jap_comb[chars[0]]=chars[1]

    '''
        load words
    '''
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
                #print(name, name[0], name[-1])
        print(len(self.words), cnt)

    '''
        find the last character from the given word
        it checks long sound symbol and small katakana
    '''
    def get_last_char(self, word):
        last = word[-1]
        if last == 'ー':
            last = self.jap_base[word[-2]]

        if last in self.jap_comb:
            last=self.jap_comb[last]

        return last

    '''
        checks if the given word meets the word chain requirements.
        If the given word is not used, then mark it as used.
        Also, get the expected character for the next turn.
    '''
    def check(self, word):
        if not word:
            return(False, 'もう使える物がないですね。')

        if self.expected_char and word[0] != self.expected_char:
            return (False, '正しくないです。')
        
        if word in self.used_words:
            return (False, '既に使ったのですよ。')
        
        if not word in self.words:
            return (False, 'ポケモンの名前ではありません。')

        if word[-1] == 'ん' or word[-1] == 'ン':
            return (False, 'ウンが付いてます。')
        
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

        return (True, 'なかなかですね。')

    '''
        pick a word based on the given word from user
        It doesn't check if picked word is ended with 'ン'
    '''
    def pick_a_word(self, word):
        if len(self.words) == 0:
            return None

        last = self.get_last_char(word)

        candidate = self.dict[last]
        if len(candidate) == 0:
            return None

        x = random.randint(0,len(candidate)-1)
        pick = candidate[x]

        return pick
        

'''
    Entry point for the word chain game
'''
game = None

def my_actions(assistant, event, device_id):
    text = event.args['text'].lower()
    print(text)

    global game

    if 'ポケモンしりとり' in text:
        assistant.stop_conversation()
        if game:
            say('既にゲームは始まってますよ。')
            return

        game = WordChain(assistant, '../data/pokemon-name.txt')
        say('じゃあ、私から始めます。')

        words = list(game.words.keys())
        x = random.randint(0,len(words)-1)
        pick = words[x]
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
'''
    for the test
'''
def test_pokemon():
    word_chain = WordChain( None, '../data/pokemon-name.txt')
    
    # user input
    test_word = input('Enter pokemon name: ')
    
    # exit condition
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
        # user typed nothing 
        if not test_word:
            inGame = False

if __name__ == '__main__':
    test_pokemon()
