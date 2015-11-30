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

def handleSentence(sentence, num):
    sentence = sentence.strip()
    words = sentence.split()
    wordTypes = []
    for i in xrange(0, len(words)):
        clearScreen()
        before = ' '.join(words[:i]) + ' '
        if i == 0:
            before = ''
        display = before + colorama.Fore.RED + words[i] \
            + colorama.Style.RESET_ALL + ' ' + ' '.join(words[i + 1:])
        word = taxonomy.sanitize(words[i])
        info = taxonomy.word(word)
        print info['definition']
        print ''
        del info['definition']
        del info['_id']
        print info
        print ''
        for j in xrange(1, len(taxonomy.TYPES)):
            print j, taxonomy.TYPES[j - 1]
        print ''
        print display
        print ''
        res = inp('What kind of word is this? ')
        if res == '':
            res = info['type'][-1]
        else:
            res = taxonomy.TYPES[int(res) - 1]
        wordTypes.append(res)
        if 'type' in info and isinstance(info['type'], list) and \
            not res in info['type']:
            info['type'].append(res)
        else:
            info['type'] = [res]
        mongo.coll.update_one({'_id': word}, {'$set': {'type': info['type']}}, \
            upsert=False)
    try:
        mongo.coll.insert_one({'_id': num, 'sentence': words, 'types': wordTypes})
    except Exception as e:
        print e
        time.sleep(1)

def main():
    allLines = taxonomy.readFile(args.args.file)
    num = 1
    for sentence in allLines.split('.'):
        if len(sentence) > 0:
            alreadyDone = taxonomy.word(num)
            if alreadyDone == None:
                handleSentence(sentence.strip(), num)
            num += 1

if __name__ == '__main__':
    main()
