import os
import sys
import copy
import pygal

import taxonomy
import mongo
import args

PUNCTUATION = {
    '?': 'Question Mark',
    '\"': 'Quotes',
    '\'': 'Quotes',
    '!': 'Exclamation Point',
    ';': 'Semicolon',
    ':': 'Colon',
    ',': 'Comma'
}

def graphAllPuntuation(sentences):
    punctuationData = {kind: [{'value': 0, 'label': PUNCTUATION[kind]} \
        for i in xrange(0, len(sentences))] \
        for kind in PUNCTUATION}
    for i in xrange(0, len(sentences)):
        for kind in PUNCTUATION:
            punctuationData[kind][i]['value'] = sentences[i].count(kind)
            if kind == '\"' or kind == '\'':
                punctuationData[kind][i]['value'] /= 2
    for i in xrange(0, len(sentences)):
        for kind in PUNCTUATION:
            punctuationData[kind][i]['label'] += ' - ' \
                + str(punctuationData[kind][i]['value'])
            if punctuationData[kind][i]['value'] < 1:
                punctuationData[kind][i]['label'] = ''
    chart = pygal.StackedBar(print_labels=True)
    chart.title = 'Punctuation By Sentence'
    num = len(sentences) + 1
    chart.x_labels = map(str, range(1, num))
    for kind in punctuationData:
        chart.add(kind, punctuationData[kind])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

def main():
    allLines = taxonomy.readFile(args.args.file)
    sentences = [sentence.strip() for sentence in allLines.split('.')]
    graphAllPuntuation(sentences)

if __name__ == '__main__':
    main()
