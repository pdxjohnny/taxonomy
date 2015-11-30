import os
import sys

import taxonomy
import mongo
import args

def wordFile(word, definition):
    insert = {
        '_id': word,
        'definition': definition
    }
    try:
        mongo.coll.insert_one(insert)
        print 'Imported', word
    except Exception as e:
        print e 

def main():
    fileHandle = open(args.args.file, 'rb')
    taxonomy.defineAll(fileHandle, wordFile)
    fileHandle.close()

if __name__ == '__main__':
    main()
