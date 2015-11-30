import os
import sys
import pygal

import taxonomy
import mongo
import args


def main():
    allWords = sorted(mongo.coll.find(), key=lambda x: x['count'], reverse=True)
    topWords = allWords[:10]
    print len(topWords)
    chart = pygal.HorizontalBar()
    chart.title = 'Most Used Words'
    chart.x_labels = map(str, range(topWords[0]['count'], topWords[-1]['count']))
    for word in topWords:
        print word['_id'], word['count']
        chart.add(word['_id'], word['count'])
    chart.render_to_png(taxonomy.outdir('most_used_words.png'))

if __name__ == '__main__':
    main()
