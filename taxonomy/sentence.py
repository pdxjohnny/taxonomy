import os
import sys
import copy
import pygal
import colorama
colorama.init()

import taxonomy
import mongo
import args
import most_used_words

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

def graphSentencePartsOfSpeech(sentences):
    num = len(sentences) + 1
    chart = pygal.StackedBar(print_labels=True)
    chart.title = 'Parts of Speech In Sentences'
    chart.x_labels = map(str, range(1, num))
    allParts = {part: [] for part in taxonomy.TYPES}
    for i in xrange(1, num):
        sentence = taxonomy.word(i)
        counts = {part: 0 for part in taxonomy.TYPES}
        for wordType in sentence['types']:
            counts[wordType] += 1
        for part in counts:
            if counts[part] != 0:
                counts[part] = {'value': counts[part], 'label': str(counts[part])}
            else:
                counts[part] = {'value': counts[part], 'label': ''}
            allParts[part].append(counts[part])
    for part in allParts:
        chart.add(part, allParts[part])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

def graphSentenceWordUse(sentences, top=0, fileName=args.args.file):
    num = len(sentences) + 1
    chart = pygal.StackedBar(print_labels=True, show_legend=False)
    chart.title = 'Word Use By Sentence'
    if top > 0:
        chart.title += ' Of Top ' + str(top) + ' Words'
        mostUsed = most_used_words.mostUsed(fileName, top=top)
        mostUsed = {word['label']: word['value'] \
            for word in mostUsed}
    chart.x_labels = map(str, range(1, num))
    sentencesByWord = [[taxonomy.sanitize(word) for word in sentence.split()] \
        for sentence in sentences]
    allWords = {}
    for sentence in sentencesByWord:
        for word in sentence:
            allWords[word] = {'label': word, 'value': 0}
    wordCounts = [copy.deepcopy(allWords) for sentence in sentencesByWord]
    for i in xrange(0, len(sentencesByWord)):
        for word in sentencesByWord[i]:
            wordCounts[i][word]['value'] += 1
    perWord = {}
    for i in xrange(0, len(wordCounts)):
        for word in wordCounts[i]:
            if not word in perWord:
                perWord[word] = []
            if wordCounts[i][word]['value'] < 1 or \
                (top > 0 and not word in mostUsed):
                wordCounts[i][word]['label'] = ''
                wordCounts[i][word]['value'] = 0
            perWord[word].append(wordCounts[i][word])
    for word in perWord:
        chart.add(word, perWord[word])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

def graphSentenceLength(sentences):
    chart = pygal.Pie(print_labels=True)
    chart.title = 'Sentence Length'
    for i in xrange(1, len(sentences) + 1):
        senLen = len(sentences[i - 1].split())
        title = str(i) + ' - ' + str(senLen) + ' words'
        senLen = {'value': senLen, 'label': str(senLen)}
        chart.add(title, [senLen])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

def main():
    allLines = taxonomy.readFile(args.args.file)
    num = 1
    sentences = [sentence.strip() for sentence in allLines.split('.')]
    graphSentenceLength(sentences)
    graphSentenceWordUse(sentences)
    graphSentenceWordUse(sentences, top=5)
    for sentence in sentences:
        if len(sentence) > 0:
            alreadyDone = taxonomy.word(num)
            if alreadyDone == None:
                handleSentence(sentence, num)
            num += 1
    graphSentencePartsOfSpeech(sentences)

if __name__ == '__main__':
    main()
