import os
import sys

import mongo
import args

def main():
    info = mongo.coll.find()
    for i in info:
        if 'definition' in i:
            del i['definition']
        print i
        print i['_id']

if __name__ == '__main__':
    main()
