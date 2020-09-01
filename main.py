from lxml import etree, html
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import re
import json # du kanske hellre vill använda YAML. Whatever floats the boat.
import sys
from pprint import pprint

# if (len(sys.argv) < 2):
#    print("Usage: main.py <restaurantName>\nEx:$> main.py pieplow")
#    sys.exit(1)
# else:
#    restaurantName = sys.argv[1]

restaurantName = "pieplow"

with open('scrapedpage.html', 'r') as fo:
    scrapedHtml = fo.read()

with open('regex.json') as json_file:
    myJson = json.load(json_file)

menuDict = {
    "Allweek" : [],
    "Monday" : [],
    "Tuesday" : [],
    "Wednesday" : [],
    "Thursday" : [],
    "Friday" : [],
}

def stringify_children(node):
    s = node.text
    if s is None:
        s = ''
    for child in node:
        r = etree.tostring(child, encoding='unicode', method='text')
        s += re.sub('( {2}|\t)', '', r)
    return s

def regexMatch(string):
    for n in range(len(myJson[restaurantName]['regex'])):
        pattern = myJson[restaurantName]['regex'][n]

        # då kollar vi om vi får en match
        match = re.findall(pattern, string, re.MULTILINE)

        if (match) and (len(match) > 0):
            # mönstret: /^((Monday|Tuesday|Wednesday|Thursday|Friday)(?::\s)([ -~åäöÅÄÖ]+))$/gm
            # ger 1st match (förhoppningsvis :)) och 3st grupper
            # grupp #1 är hela raden
            # grupp #2 är veckodagsnamn (Monday etc...)
            # grupp #3 är maträtten
            # för att kunna hantera flera rätter under en dag, tex. "Monday: Pannbiff GL HF \nKöttbullar GG NO RE"

            for n in range(len(match)):
                if(type(match[n]) == str):  # bara en match
                    menuDict['Allweek'].append(match[n])
                if(type(match[n]) == tuple):
                    day = match[n][1]
                    dish = match[n][2]
                    menuDict[day].append(dish)

def findXpath(source, xpath):
    parser = etree.HTMLParser()
    root = etree.parse(StringIO(source), parser)
    aVar = root.xpath(xpath)

    for i in aVar:
        stringify = stringify_children(i)
        if(type(stringify) == str):
            regex = regexMatch(stringify)

def parseHtml(restaurantName, scrapedHtml):
    soup = BeautifulSoup(scrapedHtml, features='lxml')

    xpaths = myJson[restaurantName]['xpath']
    regex  = myJson[restaurantName]['regex']

    for xpath in xpaths:
        findXpath(scrapedHtml, xpath)

    pprint(menuDict, width=999) # gör om det till JSON eller YAML eller whatever...

parseHtml(restaurantName, scrapedHtml)