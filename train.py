# -*- coding: utf-8 -*-
from preprocessor import Preprocessor
import os


class Train:

    def __init__(self, n, lang, smooth=0.5):
        self.n = n
        self.lang = lang
        self.frequency = dict()
        self.probability = dict()
        self.smooth = smooth
        preprocessor = Preprocessor()
        preprocessor.run()

    def run(self):
        self.__create_dictionary__()
        self.__calculate_gram_probability__()
        self.__dump_model__()

    def __create_dictionary__(self):
        data_file_list = list()
        # select lang data
        for file_name in os.listdir('temp'):
            if file_name.split('-')[0] == self.lang:
                data_file_list.append('temp/' + file_name)
        # create dictionary
        for file_name in data_file_list:
            with open(file_name, 'r+', encoding='utf-8', errors='ignore') as corpus:
                # for every term in the corpus
                for term in corpus.read().split():
                    # for every character in the term
                    for i in range(len(term) - self.n + 1):
                        # create term and set frequency, or increase by 1 if it exists
                        self.frequency[term[i:(i + self.n)]] = self.frequency.get(term[i:(i + self.n)], 0) + 1

    def __calculate_gram_probability__(self):
        # denominator = total number of the frequencies of all grams + size of gram vocabulary x smooth
        denominator = float(sum(self.frequency.values())) + (float(len(self.frequency)) * float(self.smooth))
        for gram, frequency in self.frequency.items():
            # numerator = frequency of a gram + smoothing
            numerator = float(frequency) + float(self.smooth)
            # calculate the probability and add it to the probability dict
            self.probability[gram] = float(numerator) / float(denominator)

    def __dump_model__(self):
        if self.n == 1:
            prefix = 'unigram'
        elif self.n == 2:
            prefix = 'bigram'
        else:
            prefix = self.n + 'gram'
        with open('output/' + prefix + self.lang.upper() + '.txt', 'w+', encoding='utf-8', errors='ignore') as model:
            for gram in sorted(self.probability):
                model.write('P(' + gram + ') = ' + str(self.probability[gram]) + '\n')


