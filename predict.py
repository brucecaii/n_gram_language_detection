from preprocessor import Preprocessor
import os
import math
import pickle
import re


language = {
    'EN': 'English',
    'FR': 'French'
}
model_type = {
    1: 'unigram',
    2: 'bigram'
}


class Predict:

    def __init__(self, n, smooth=0.5):
        self.smooth = smooth
        self.n = n
        self.model_list = self.__load_model__()
        if n < 1 or n > 2:
            print('Only support unigram or bigram.')
            os._exit(1)
        if len(self.model_list) == 0:
            print('Please train first.')
            os._exit(1)

    def run(self):
        p = Preprocessor('test/')
        p.run()
        for file_name in os.listdir('temp/'):
            with open('temp/' + file_name, 'r+', encoding='utf-8', errors='ignore') as test_file:
                for idx, sentence in enumerate(filter(None, test_file.read().split('\n'))):
                    # run prediction on every model
                    print_log = list()
                    sentence_probabilities = dict()
                    for model in self.model_list:
                        sentence_probability, log = self.__calculate_sentence_probability__(sentence, model)
                        print_log.append(log)
                        sentence_probabilities[model['lang']] = sentence_probability
                    detected = language[sorted(sentence_probabilities, key=lambda x: sentence_probabilities[x])[-1]
                        .upper()]
                    self.__save_trace__(sentence, idx, print_log, detected)

    def __calculate_sentence_probability__(self, sentence, model):
        log = list()
        # append boundary when n = 2
        # treat the sentence as a word since all just addition
        # i.e. #birds#build#nests#
        if model['n'] == 2:
            p_sentence = '#'.join(filter(None, sentence.split()))
            p_sentence = '#' + p_sentence + '#'
        else:
            p_sentence = ''.join(filter(None, sentence.split()))
        # get ['#b', 'bi', 'ir' 'rd', 'd#' ...., 's#']
        grams = [p_sentence[i:i + model['n']] for i in range(len(p_sentence) - model['n'] + 1)]
        # get the probabilities of each gram
        sentence_probability = 0
        for gram in grams:
            log.append({
                gram: list()
            })
            # if the gram is in the dictionary, get the probability
            if gram in model['probability']:
                gram_probability = model['probability'][gram]
            # if not, calculate the add delta value
            else:
                denominator = float(model['size']) + (
                        float(len(model['probability'])) * float(self.smooth))
                numerator = float(self.smooth)
                gram_probability = numerator / denominator
            sentence_probability += math.log(gram_probability, 10)
            log[-1][gram].append(language[model['lang'].upper()].upper() + ': P(' + '|'
                                 .join(reversed([char for char in gram]))
                                 + ') = ' + str(gram_probability) + '  ==> log prob of sentence so far: '
                                 + str(sentence_probability))
        return sentence_probability, log

    def __load_model__(self):
        model_list = list()
        prefix = model_type[1] if self.n == 1 else model_type[2]
        for file_name in os.listdir('output/'):
            if re.match(prefix, file_name) and file_name.endswith('.pkl'):
                with open('output/' + file_name, 'rb+') as model:
                    model_list.append(pickle.load(model))
        return model_list

    def __save_trace__(self, sentence, idx, print_log, detected):
        with open('output/out' + str(idx + 1) + '.txt', 'a+', encoding='utf-8', errors='ignore') as st_log:
            st_log.write(sentence + '\n\n')
            st_log.write(model_type[self.n].upper() + ' MODEL:\n')
            for j in range(len(print_log[0])):
                for gram, gram_log in print_log[0][j].items():
                    st_log.write('\n' + model_type[self.n].upper() + ': ' + gram + '\n')
                    for i in range(len(print_log)):
                        for s in print_log[i][j].values():
                            st_log.write(s[0] + '\n')
            st_log.write('According to the ' + model_type[self.n] + ' model, the sentence is in ' + detected)
            print(sentence + ' [' + detected + ']')
            st_log.write('\n----------------\n')



