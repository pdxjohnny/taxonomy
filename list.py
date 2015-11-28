import os
import sys

import mongo

def main():
    for word in mongo.coll.find():
        if not 'count' in word:
            continue
        print word['_id'], word['count']

if __name__ == '__main__':
    main()
