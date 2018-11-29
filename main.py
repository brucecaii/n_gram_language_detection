# -*- coding: utf-8 -*-
from cli import Cli
from train import Train
from predict import Predict
import os
import shutil

if __name__ == '__main__':

    if not os.path.isdir('output'):
        os.mkdir('output')
    # reset
    if os.path.isdir('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')
    # create cli
    args = Cli.create_parser().parse_args()
    if args.subparser_name == 'train':
        t = Train(int(args.model), args.lang)
        t.run()
    else:
        p = Predict(int(args.model))
        p.run()
