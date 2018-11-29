from preprocessor import Preprocessor
import os
import re
import math
import pickle


class Predict:

    def __init__(self, n):
        self.n = n
        if self.n == 1:
            prefix = 'unigram'
        elif self.n == 2:
            prefix = 'bigram'
        else:
            prefix = str(self.n) + 'gram'
        self.model_list = self.__load_model__(prefix)
        print(self.model_list)
        if len(self.model_list) == 0:
            print('Please train first.')
            os._exit(1)

    def run(self):
        p = Preprocessor('test/')
        p.run()
        for file_name in os.listdir('temp/'):
            with open('temp/' + file_name, 'r+', encoding='utf-8', errors='ignore') as test_file:
                for sentence in test_file.read().split('\n'):
                    if sentence == '':
                        continue
                    result = self.__calculate_sentence_probability__(sentence)

    def __load_model__(self, prefix):
        model_list = dict()
        for file_name in os.listdir('output/'):
            print(file_name)
            if re.match(prefix, file_name) and file_name.endswith('.pkl'):
                with open('output/' + file_name, 'rb+') as model:
                    lang = file_name.replace(prefix, '').replace('.pkl', '')
                    model_list[lang] = pickle.load(model)
        return model_list

    def __calculate_sentence_probability__(self, sentence):
        sentence_probability = dict()
        for lang in self.model_list.keys():
            sentence_probability[lang] = 0
            for term in sentence.split():
                if term == '':
                    continue
                sentence_probability[lang] += self.__calculate_term_probability(term, lang)
                break
            break
        return sentence_probability

    def __calculate_term_probability(self, term, lang):
        if self.n > 1:
            term = '#' + term + '#'
        grams = [term[i:i + self.n] for i in range(len(term) - self.n + 1)]
        term_probability = 0
        for gram in grams:
            term_probability += math.log(self.model_list[lang][gram])
        return 0


