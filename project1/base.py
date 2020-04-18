#!/usr/bin/env python
import codecs
import math
import re
import time
import sys

from bs4 import BeautifulSoup

totalFiles = []
frequencyTokens = {}
allTermFrequency = {}
totalCases = 0
totalDocuments = 503

givenTokens = []

for arg in sys.argv:
    givenTokens.append(arg)

# remove the path
givenTokens.pop(0)

startTime = time.time()

# gets all the stop words
stopFile = open('stoplist.txt', 'r')
stops = stopFile.readlines()
stopwords = [x.strip() for x in stops]
stopwords = set(stopwords)
emptyFiles = []

# iterate through the local html files
for num in range(1, totalDocuments):
    stringNum = str(num)
    if 100 > num > 9:
        stringNum = "0" + stringNum
    elif num < 10:
        stringNum = "00" + stringNum

    file = codecs.open("files/" + stringNum + ".html", 'r', encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(file, 'html.parser')
    file.close()

    # Get as text and split up the words without any case issues and newlines
    results = soup.text
    results = results.strip()
    results = results.lower()
    results = re.sub('\W+', ' ', results)
    allWords = results.split(" ")
    localFrequencyTokens = {}

    specialCheck = re.compile('[@_\[\]#$%^&*()<>/\}{~1234567890-]')

    for word in allWords:
        # Check for special characters that didnt get expunged
        if specialCheck.search(word) is not None:
            # Do nothing
            pass
        # increase to local dictionary if new key or create a new one if it's new, same with the larger dictionary
        elif word in localFrequencyTokens:
            localFrequencyTokens[word] = localFrequencyTokens[word] + 1
            if word in frequencyTokens:
                frequencyTokens[word] = frequencyTokens[word] + 1
            else:
                frequencyTokens[word] = 1
        else:
            localFrequencyTokens[word] = 1
            if word in frequencyTokens:
                frequencyTokens[word] = frequencyTokens[word] + 1
            else:
                frequencyTokens[word] = 1

    # remove stopwords in frequencyToken dictionary
    for stopword in stopwords:
        if stopword in frequencyTokens:
            localFrequencyTokens.pop(stopword)
            frequencyTokens.pop(stopword)

    # removes '' words
    if '' in localFrequencyTokens:
        localFrequencyTokens.pop('')

    # calculate the term frequency of every word in the file and save to a dictionary
    fileSize = len(localFrequencyTokens)
    termFreq = {}

    # only calc the given words
    for word in givenTokens:
        if word in localFrequencyTokens:
            termFreq[word] = localFrequencyTokens[word] / float(fileSize)
        else:
            emptyFiles.append(num)

    # dictionary for all termFrequency of all the files
    allTermFrequency[num] = termFreq

    # unused
    totalFiles.append(localFrequencyTokens)

# removes '' words
if '' in frequencyTokens:
    frequencyTokens.pop('')

# calculate the inverse frequency
inverseDocumentFreq = {}

for word in givenTokens:
    inverseDocumentFreq[word] = math.log(totalDocuments / float(frequencyTokens[word]))

weightDocPair = {}

for num in range(1, totalDocuments):
    if num in emptyFiles:
        pass
    else:
        stringNum = str(num)
        if 100 > num > 9:
            stringNum = "0" + stringNum
        elif num < 10:
            stringNum = "00" + stringNum
        termFreq = allTermFrequency[num]
        totalGivenWordWeight = 0
        # if all the words exists in the current document, save doc, word weight sum
        for word in givenTokens:
            if word in termFreq:
                # for each term in a file, calculate the weight of each word by tf-idf and save to total
                totalGivenWordWeight = totalGivenWordWeight + (termFreq[word] * inverseDocumentFreq[word])

        weightDocPair[num] = totalGivenWordWeight

for file in weightDocPair:
    print(str(file) + ': ' + str(weightDocPair[file]) + '\n')

endTime = time.time()
seconds = endTime - startTime
print('trial: ' + str(seconds) + ' seconds')
