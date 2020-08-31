from lxml import etree, html
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import re
import json
import sys

# if (len(sys.argv) < 2):
#    print("Usage: main.py <restaurantName>\nEx:$> main.py pieplow")
#    sys.exit(1)
# else:
#    restaurantName = sys.argv[1]

restaurantName = "pieplow"
with open('scrapedpage.html', 'r') as fo:
    scrapedHtml = fo.read()

def stringify_children(node):
    s = node.text
    if s is None:
        s = ''
    for child in node:
        r = etree.tostring(child, encoding='unicode', method='text')
        s += re.sub('( {2}|\t)', '', r)
    return s.strip()

def findXpath(source, xpath):
    parser = etree.HTMLParser()
    root = etree.parse(StringIO(source), parser)
    aVar = root.xpath(xpath)

    r = ''

    for i in aVar:
        r += stringify_children(i)
        # regexmatcha

    return r

def parseHtml(restaurantName, scrapedHtml):
    soup = BeautifulSoup(scrapedHtml, features='lxml')

    with open('regex.json') as json_file:
        myJson = json.load(json_file)

    xpaths = myJson[restaurantName]['xpath']
    regex  = myJson[restaurantName]['regex']

    finalChunk = ''

    for xpath in xpaths:
        aStr = findXpath(scrapedHtml, xpath)
        if(type(aStr) == str):
            finalChunk += aStr

    print(finalChunk)




parseHtml(restaurantName, scrapedHtml)