# -*- coding: utf-8 -*-
import os
import re


class Preprocessor:

    def __init__(self, path='corpus/'):
        self.symbol = r'\,|\.|\!|\?|\$|\&|\/|\\|\-|\+|\@|\(|\)|\<|\>|\{|\}|\#|\*|\:|\;|\"|\”|\“|\s\'|\_|\[|\]|\||\%|\='
        self.path = path

    def run(self):
        for file_name in os.listdir(self.path):
            processed_corpus = ''
            with open(self.path + file_name, 'r+', encoding='utf-8', errors='ignore') as corpus:
                for line in corpus.readlines():
                    # remove numbers
                    line = re.sub(r'\d+', '', line)
                    # remove symbols
                    line = re.sub(self.symbol, ' ', line)
                    # remove "'" from words
                    line = re.sub(r'\'', '', line)
                    # strip out extra spaces
                    line = re.sub(r'\s+', ' ', line).strip(' ')
                    # lowercase
                    line = line.lower()
                    # remove empty lines and numbers
                    if line == '':
                        continue
                    if self.path == 'test/':
                        processed_corpus += line + '\n'
                    else:
                        processed_corpus += line + ' '
            with open('temp/' + file_name, 'w+', encoding='utf-8') as corpus:
                corpus.write(processed_corpus)
