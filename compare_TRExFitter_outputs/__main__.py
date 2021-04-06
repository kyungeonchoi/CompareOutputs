import argparse
from . import compare_root

parser = argparse.ArgumentParser(description='Provide two TREx output folders for comparison.')
parser.add_argument('first', metavar='first_path', type=str, help='path to the first folder')
parser.add_argument('second', metavar='second_path', type=str, help='path to the second folder')

args = parser.parse_args()

input_path_1 = args.first
input_path_2 = args.second

try: 
    compare_root(input_path_1, input_path_2)
except:
    print('Something went wrong...')
