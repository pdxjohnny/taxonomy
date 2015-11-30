import os
import urllib
import urllib2
import xml.etree.ElementTree as ET

import args
import mongo

def word(string):
    return mongo.coll.find_one({"_id": string})

def readFile(path):
    fileHandle = open(path, 'rb')
    data = fileHandle.read()
    fileHandle.close()
    return data

def outdir(fileName=''):
    if not os.path.exists(args.args.outdir):
        os.mkdir(args.args.outdir)
    return os.path.join(args.args.outdir, fileName)

def sanitize(word):
    word = word.lower()
    word = noPuncuation(word)
    return word

def noPuncuation(word):
    for i in xrange(0, 128):
        if not ((i >= 65 and i <= 90) or (i >= 97 and i <= 121) or i == 32):
            word = word.replace(chr(i), '')
    return word

def define(word):
    url = 'http://services.aonaware.com/DictService/DictService.asmx/Define'
    values = {
        'word': word
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    data = response.read()

    return ET.fromstring(data)

def defineAll(fileObj, callback):
    for line in fileObj:
        for word in line.split():
            word = sanitize(word)
            results = define(word)
            if len(results) > 1:
                allDefinitions = []
                for definition in list(results[1]):
                    if len(definition) > 2:
                        allDefinitions.append(definition[2].text)
                callback(word, '\n'.join(allDefinitions))
