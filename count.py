import os
import sys
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['word-database']
worddb = db['word-collection']

def main():
    for line in sys.stdin:
        for word in line.split():
            word = word.tolower()
            worddb.update_one({'_id': word}, {'$inc': {'count': 1}})

if __name__ == '__main__':
    main()
