from cli import Cli
import os

if __name__ == '__main__':

    if not os.path.isdir('output'):
        os.makedirs('output')
    args = Cli.create_parser().parse_args()
    if args.subparser_name == 'train':
        pass
    else:
        pass
