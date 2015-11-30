import os
import sys

import taxonomy
import mongo
import args

def main():
    word = args.args.word
    try:
        word = int(word)
    except Exception as e:
        pass
    info = taxonomy.word(word)
    if 'definition' in info:
        definition = info['definition']
        del info['definition']
        print definition
        print ''
    print info
    print ''
    print info['_id']
    if args.args.set != '':
        to = args.args.to
        try:
            to = int(to)
        except Exception as e:
            pass
        mongo.coll.update_one({'_id': info['_id']}, \
            {'$set': {args.args.set: to}}, \
            upsert=False)

if __name__ == '__main__':
    main()
