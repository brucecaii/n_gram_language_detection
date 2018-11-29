# -*- coding: utf-8 -*-
from argparse import ArgumentParser


class Cli:

    @staticmethod
    def create_parser():
        # create the main parser for CLI
        command_parser = ArgumentParser(prog='N-gram language detector')
        # create branches for train and predict
        method_parsers = command_parser.add_subparsers(help='[command] help',
                                                       dest='subparser_name')
        method_parsers.required = True
        # create a general template for methods
        template_parser = ArgumentParser(add_help=False,
                                         conflict_handler='resolve')
        template_parser.add_argument('-n',
                                     dest='model',
                                     action='store',
                                     metavar='INT',
                                     help='Specify the n-gram model.',
                                     required=True)
        # train
        train_parser = method_parsers.add_parser('train',
                                                 parents=[template_parser],
                                                 help='Train with data set.')
        train_parser.add_argument('-l',
                                  dest='lang',
                                  action='store',
                                  metavar='en, fr',
                                  help='Specify the language to train.',
                                  required=True)
        # predict
        predict_parser = method_parsers.add_parser('predict',
                                                   parents=[template_parser],
                                                   help='Predict with model.')
        return command_parser

