import os
import sys

import taxonomy
import mongo

def wordFile(word, definition):
    insert = {
        '_id': word,
        'definition': definition
    }
    try:
        mongo.coll.insert_one(insert)
    except Exception as e:
        print e 

def main():
    taxonomy.defineAll(sys.stdin, wordFile)

if __name__ == '__main__':
    main()
