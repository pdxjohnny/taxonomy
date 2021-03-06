import os
import sys
import copy
import pygal
import colorama
colorama.init()

import taxonomy
import mongo
import args

try:
    inp = raw_input
except:
    inp = input

CLAUSE_KINDS = [
    'independent',
    'dependent'
]

SENTENCE_KINDS = {
    'simple': {'independent': 1, 'dependent': 0},
    'compound': {'independent': 2, 'dependent': 0},
    'complex': {'independent': 1, 'dependent': 1},
    'compound-complex': {'independent': 2, 'dependent': 1}
}

try:
    inp = raw_input
except:
    inp = input

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

def handleSentence(sentence, num):
    clearScreen()
    print sentence
    print ''
    for clause in CLAUSE_KINDS:
        numOfClause = int(inp('How many ' + clause \
            + ' clauses in this sentence? '))
        mongo.coll.update_one({'_id': num}, {'$set': {clause: numOfClause}}, \
            upsert=False)
        print ''

def graphSentenceClauses(sentences):
    num = len(sentences) + 1
    chart = pygal.StackedBar(print_labels=True)
    chart.title = 'Sentence Clauses'
    chart.x_labels = map(str, range(1, num))
    allClauses = {clause: [] for clause in CLAUSE_KINDS}
    for i in xrange(1, num):
        sentence = taxonomy.word(i)
        for clause in CLAUSE_KINDS:
            if sentence[clause] != 0:
                sentence[clause] = {'value': sentence[clause], 'label': str(sentence[clause])}
            else:
                sentence[clause] = {'value': sentence[clause], 'label': ''}
            allClauses[clause].append(sentence[clause])
    for clause in allClauses:
        chart.add(clause, allClauses[clause])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

def graphSentenceKinds(sentences):
    num = len(sentences) + 1
    chart = pygal.StackedBar()
    chart.title = 'Kinds Of Sentences'
    chart.x_labels = map(str, range(1, num))
    allKinds = {kind: [] for kind in SENTENCE_KINDS}
    for i in xrange(1, num):
        sentence = taxonomy.word(i)
        for kind in SENTENCE_KINDS:
            if sentence['dependent'] == SENTENCE_KINDS[kind]['dependent'] and \
                sentence['independent'] == SENTENCE_KINDS[kind]['independent']:
                sentenceKind = {'value': 1, 'label': kind}
            else:
                sentenceKind = {'value': 0, 'label': ''}
            allKinds[kind].append(sentenceKind)
    for kind in allKinds:
        chart.add(kind, allKinds[kind])
    fileName = chart.title.lower().replace(' ', '_')
    chart.render_to_png(taxonomy.outdir(fileName + '.png'))

def main():
    allLines = taxonomy.readFile(args.args.file)
    num = 1
    sentences = [sentence.strip() for sentence in allLines.split('.')]
    for sentence in sentences:
        if len(sentence) > 0:
            alreadyDone = taxonomy.word(num)
            if alreadyDone == None or \
                not 'independent' in alreadyDone or \
                not 'dependent' in alreadyDone:
                handleSentence(sentence, num)
            num += 1
    graphSentenceClauses(sentences)
    graphSentenceKinds(sentences)

if __name__ == '__main__':
    main()
