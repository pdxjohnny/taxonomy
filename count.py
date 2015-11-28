import os
import sys

import taxonomy
import mongo

def main():
    for line in sys.stdin:
        for word in line.split():
            word = word.lower()
            word = taxonomy.noPuncuation(word)
            mongo.coll.update_one({'_id': word}, {'$inc': {'count': 1}})

if __name__ == '__main__':
    main()
