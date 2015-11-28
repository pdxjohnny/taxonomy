import urllib
import urllib2
import xml.etree.ElementTree as ET

def noPuncuation(word):
    for i in xrange(0, 128):
        if not ((i >= 65 and i <= 90) or (i >= 97 and i <= 121) or i == 32):
            word = word.replace(chr(i), '')
    return word

def define(word):
    url = 'http://services.aonaware.com/DictService/DictService.asmx/DefineInDict'
    values = {
        'word': word,
        'dictId': 'wn'
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    data = response.read()

    return ET.fromstring(data)

def defineAll(fileObj, callback):
    for line in fileObj:
        for word in line.split():
            word = word.lower()
            word = noPuncuation(word)
            results = define(word)
            if len(results) > 1:
                allDefinitions = []
                for definition in list(results[1]):
                    if len(definition) > 2:
                        allDefinitions.append(definition[2].text)
                callback(word, '\n'.join(allDefinitions))
