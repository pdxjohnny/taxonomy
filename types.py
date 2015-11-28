import os
import sys
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['word-database']
worddb = db['word-collection']

def main():
    for word in worddb.find():
        if not 'count' in word:
            continue
        print word['_id'], word['count']

if __name__ == '__main__':
    main()
