import os
import sys

import taxonomy
import args

def main():
    info = taxonomy.word(taxonomy.sanitize(args.args.word))
    definition = info['definition']
    del info['definition']
    print info['_id']
    print info
    print ''
    print definition
    print ''

if __name__ == '__main__':
    main()
