#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from collections import defaultdict

import os
import random
import re
import sys

'''
    Word chain game
'''
class WordChain(object):
    '''
        builds words dictionary and required files
    '''
    def __init__(self, words_file):
        self._jap_base = dict()
        self._jap_comb = dict()

        self._words = dict()
        self._dict = defaultdict(list)
        self._used_words = dict()
        self._expected_char=None

        path=os.path.realpath(__file__)
        bin='bin/'+__file__.rsplit('/', 1)[1]
        self._data_dir = path.replace(bin,"data/")

        self._load_gojuon()
        self._load_combination()

        self._load_words(words_file)

    def _load_gojuon(self):
        '''
            load mappings for the long sound
        '''
        with open(self._data_dir + 'gojuon.txt', 'r') as input:
            for line in input:
                chars = line.strip().split(',')
                base = chars[0]
                chars.pop(0)
                for char in chars:
                    self._jap_base[char]=base

    def _load_combination(self):
        '''
            load mappings for small katakana
        '''
        with open(self._data_dir + 'combination.txt', 'r') as input:
            for line in input:
                chars = line.strip().split(',')
                self._jap_comb[chars[0]]=chars[1]

    def _load_words(self, file):
        '''
            load words
        '''
        cnt = 0
        ptn = re.compile(r"([・：]|\(.*?\))")
        with open(self._data_dir+file, 'r') as input:
            for line in input:
                word_tuple = line.strip().split(',')
                name = word_tuple[1]
                word_tuple.pop(1)
                name = ptn.sub('', name).strip()
                self._words[name] = word_tuple
                self._dict[name[0]].append(name)
                cnt += 1
                #print(name, name[0], name[-1])
        print(len(self._words), cnt)

    def _get_last_char(self, word):
        '''
        find the last character from the given word
        it checks long sound symbol and small katakana
        '''
        last = word[-1]
        if last == 'ー':
            last = self._jap_base[word[-2]]

        if last in self._jap_comb:
            last = self._jap_comb[last]

        return last

    def check(self, word):
        '''
        checks if the given word meets the word chain requirements.
        If the given word is not used, then mark it as used.
        Also, get the expected character for the next turn.
        '''
        if not word:
            return(False, 'もう使える物がないですね。')

        if self._expected_char and word[0] != self._expected_char:
            return (False, '正しくないです。')
        
        if word in self._used_words:
            return (False, '既に使ったのですよ。')
        
        if not word in self._words:
            return (False, 'ポケモンの名前ではありません。')

        if word[-1] == 'ん' or word[-1] == 'ン':
            return (False, 'ウンが付いてます。')
        
        self._used_words[word] = self._words[word]
        del self._words[word]

        idx = 0
        list = self._dict[word[0]]
        for x in list:
            if x == word:
                del list[idx]
                break
            idx +=1 

        self._expected_char=self._get_last_char(word)

        return (True, 'なかなかですね。')

    def pick_a_word(self, word=None):
        '''
        pick a word based on the given word from user
        It doesn't check if picked word is ended with 'ン'
        '''
        if not word:
            words = list(self._words.keys())
            x = random.randint(0,len(words)-1)
            return words[x]

        if len(self._words) == 0:
            return None

        last = self._get_last_char(word)

        candidate = self._dict[last]
        if len(candidate) == 0:
            return None

        x = random.randint(0,len(candidate)-1)
        pick = candidate[x]

        return pick
        

'''
    for the test
'''
def test_pokemon():
    word_chain = WordChain( None, 'pokemon-name.txt')
    
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
