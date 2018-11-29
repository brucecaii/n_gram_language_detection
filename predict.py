import os
import re


class Predict:

    def __init__(self, n):
        if n == 1:
            prefix = 'unigram'
        elif n == 2:
            prefix = 'bigram'
        else:
            prefix = str(n) + 'gram'
        self.model_list = self.__load_model__(prefix)
        if len(self.model_list) == 0:
            print('Please train first.')
            os._exit(1)
        print(self.model_list)

    def run(self):
        print(self.model_list)

    def __load_model__(self, prefix):
        model_list = dict()
        for file_name in os.listdir('output/'):
            if re.match(prefix, file_name):
                with open('output/' + file_name, 'r+', encoding='utf-8', errors='ignore') as model:
                    lang = file_name.replace(prefix, '').replace('.txt', '')
                    model_list[lang] = dict()
                    for line in model.read().split('\n'):
                        if line == '':
                            continue
                        gram = line.split(') = ')[0].replace('P(', '')
                        probability = float(line.split(') = ')[1])
                        model_list[lang][gram] = probability
        return model_list

