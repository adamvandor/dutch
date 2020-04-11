import requests
import urllib
from bs4 import BeautifulSoup
import argparse
import urllib.request
import re
import json
from random import shuffle
from pandas import DataFrame

parser = argparse.ArgumentParser()
parser.add_argument('--n_phrases', type=int, default=1000)
parser.add_argument('--save', type=str, default='')
args = parser.parse_args()

def generate_random_phrase():
    r1 = requests.get('http://www.smartphrase.com/cgi-bin/randomphrase.cgi?dutch&serious&normal&30&140&124&39&167&96')
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, 'html.parser')
    coverpage_news = soup1.find_all()
    translation_ends = '<p></p></p></td></tr>\n<tr>'
    translation_starts = '>\n'
    raw_html_code = str(coverpage_news)
    end_points = [m.start() for m in re.finditer(translation_ends, raw_html_code)]
    first_end_point = end_points[0]
    j = first_end_point - 2
    c, text = '', ''
    while c != '\n':
        c = raw_html_code[j]
        text += c
        j -= 1
        c = raw_html_code[j]
    text = text[::-1]
    dutch, english = text.split('<p>')
    return dutch, english
    
def build_dictionary():
    english_keys_dictionary = {}
    for i in range(args.n_phrases):
        if i % 10 == 0:
            print('Downloading... {:.2f}%'.format(i / args.n_phrases * 100))
        d, e = generate_random_phrase()
        if e not in english_keys_dictionary.keys():
            english_keys_dictionary[e] = d
    print('\n{} duplicates dropped. \n{} unique phrases in dictionary.\n'.format(args.n_phrases - len(english_keys_dictionary), len(english_keys_dictionary)))
    dutch_keys_dictionary = dict((v,k) for k,v in english_keys_dictionary.items()) 
    return english_keys_dictionary, dutch_keys_dictionary
    
def practice(dictionary):
    keys = list(dictionary.keys())
    shuffle(keys)
    a = ''
    i = 0
    while a == '':
        print('=== {} ===============================================\n'.format(i + 1))
        a = input('English: \n         {}'.format(keys[i]))
        if a == '':
            print('Dutch:   \n         {}'.format(dictionary[keys[i]]))
        print()
        i += 1

if __name__ == '__main__':
    e_dict, d_dict = build_dictionary()
    if args.save != '':
        with open(args.save, 'w') as f:
            f.write(DataFrame(e_dict.items(), columns=['English', 'Dutch']).to_string())
    practice(e_dict)
    
