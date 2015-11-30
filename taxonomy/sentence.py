import os
import sys
import colorama
colorama.init()

import taxonomy
import mongo
import args

try:
    inp = raw_input
except:
    inp = input

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

def handleSentence(sentence):
    sentence = sentence.strip()
    words = sentence.split()
    for i in xrange(0, len(words)):
        clearScreen()
        before = ' '.join(words[:i]) + ' '
        if i == 0:
            before = ''
        display = before + colorama.Fore.RED + words[i] \
            + colorama.Style.RESET_ALL + ' ' + ' '.join(words[i + 1:])
        print display
        print ''
        word = taxonomy.sanitize(words[i])
        info = taxonomy.word(word)
        print info['definition']
        print ''
        res = inp('What kind of word is this? ')
        mongo.coll.update_one({'_id': word}, {'$set': {'type': res}}, \
            upsert=False)

def main():
    allLines = taxonomy.readFile(args.args.file)
    for sentence in allLines.split('.'):
        if len(sentence) > 0:
            handleSentence(sentence.strip())

if __name__ == '__main__':
    main()
