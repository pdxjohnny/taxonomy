import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--outdir', help='Directory to output to', \
    default='out')
parser.add_argument('--file', help='Input file', \
    default='section')
parser.add_argument('--word', help='Word to look up')

if sys.argv[0] == 'python -m unittest':
    args = parser.parse_args([])
else:
    args = parser.parse_args()
