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
    try:
        mongo.coll.update_one({'_id': word}, {'$inc': {'count': 1}})
    except Exception as e:
        print e 

def main():
    fileHandle = open(args.args.file, 'rb')
    taxonomy.defineAll(fileHandle, wordFile)
    fileHandle.close()

if __name__ == '__main__':
    main()
