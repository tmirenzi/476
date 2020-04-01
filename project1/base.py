import codecs
import math
import re
import time

from bs4 import BeautifulSoup

if __name__ == '__main__':

    totalFiles = []
    frequencyTokens = {}
    allTermFrequency = {}
    totalCases = 0
    totalDocuments = input("Enter the under of documents to be weighed: ")
    totalDocuments = int(totalDocuments) + 1

    startTime = time.time()

    # gets all the stop words
    stopFile = open('stoplist.txt', 'r')
    stops = stopFile.readlines()
    stopwords = [x.strip() for x in stops]
    stopwords = set(stopwords)

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

        for word, count in localFrequencyTokens.items():
            termFreq[word] = count / float(fileSize)

        # dictionary for all termFrequency of all the files
        allTermFrequency[num] = termFreq

        # unused
        totalFiles.append(localFrequencyTokens)

    # removes '' words
    if '' in frequencyTokens:
        frequencyTokens.pop('')

    # calculate the inverse frequency
    inverseDocumentFreq = {}

    for word, val in frequencyTokens.items():
        inverseDocumentFreq[word] = math.log(totalDocuments / float(val))

    # term dictionary that has the length of the the list of document-weight pairs of a term
    termSizePair = {}
    # Create postings file
    filePath = 'C:/Users/Tony/PyCharmProjects/476/project1/proj3/postings.txt'
    file = open(filePath, 'w', encoding='utf-8', errors='ignore')

    # TODO: optional sort by alphabet
    for word in frequencyTokens:
        termDocWeightPair = []
        set(termDocWeightPair)
        for num in range(1, totalDocuments):
            stringNum = str(num)
            if 100 > num > 9:
                stringNum = "0" + stringNum
            elif num < 10:
                stringNum = "00" + stringNum
            termFreq = allTermFrequency[num]

            # if the word exists in the current document, save doc, word weight pair
            if word in termFreq:
                # for each term in a file, calculate the weight of each word by tf-idf and save to a vector
                docWeightPair = str(num) + ", " + str(termFreq[word] * inverseDocumentFreq[word])
                termDocWeightPair.append(docWeightPair)
        termSizePair[word] = termDocWeightPair
        # writing the pair to the postings text file
        # file.write(str(word) + ': \n')
        for pair in termDocWeightPair:
            file.write(str(pair) + '\n')

    file.close()

    filePath = 'C:/Users/Tony/PyCharmProjects/476/project1/proj3/dictionaryRecord.txt'
    file = open(filePath, 'w', encoding='utf-8', errors='ignore')
    wordPosition = 1
    for word in termSizePair:
        file.write(word + '\n')
        length = termSizePair[word]
        file.write(str(len(length)) + '\n')
        file.write(str(wordPosition) + '\n')
        wordPosition = len(length) + wordPosition
    file.close()

    endTime = time.time()
    seconds = endTime - startTime
    print('trial: ' + str(seconds) + ' seconds')
