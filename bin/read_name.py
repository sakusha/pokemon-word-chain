#!/home/pi/assistant-sdk-python/google-assistant-sdk/env/bin/python3

from google_speech import Speech

def read_pokemon():
    with open('../data/pokemon-name.txt', 'r') as input:
        for line in input:
            pokemon_tuple = line.strip().split(',')
            #print(pokemon_tuple)
            Speech(pokemon_tuple[1], 'ja').play(None)


if __name__ == '__main__':
    read_pokemon()
