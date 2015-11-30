import os
import sys
import pygal

import taxonomy
import mongo
import args

def mostUsed(fileName, top=10):
    fileData = taxonomy.readFile(fileName)
    section = [taxonomy.sanitize(word) for word in fileData.split()]
    wordCounts = {word: 0 for word in section}
    for word in section:
        wordCounts[word] += 1
    allWords = [{'label': word, 'value': wordCounts[word]} \
        for word in wordCounts]
    allWords = sorted(allWords, key=lambda x: x['value'], reverse=True)
    topWords = allWords[:top]
    return topWords

def main():
    topWords = mostUsed(args.args.file, top=10)
    chart = pygal.Pie(print_labels=True)
    chart.title = 'Most Used Words'
    for word in topWords:
        title = word['label']
        word['label'] += ' - ' + str(word['value'])
        chart.add(title, [word])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

if __name__ == '__main__':
    main()
