#!/usr/bin/python

with open('../data/pokemon-name.txt', 'r') as input:
    for line in input:
        pokemon_tuple = line.strip().split(',')
        print(pokemon_tuple)
