import os
import sys

import taxonomy
import args

def main():
    info = taxonomy.word(args.args.word)
    if 'definition' in info:
        definition = info['definition']
        del info['definition']
        print definition
        print ''
    print info
    print ''
    print info['_id']

if __name__ == '__main__':
    main()
