#!/usr/bin/env python
import codecs
import math
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc

from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from scipy import sparse

if __name__ == '__main__':

    totalFiles = []
    frequencyTokens = {}
    allTermFrequency = {}
    totalCases = 0
    totalDocuments = 504

    startTime = time.time()

    # gets all the stop words
    stopFile = open('stoplist.txt', 'r')
    stops = stopFile.readlines()
    stopwords = [x.strip() for x in stops]
    stopwords = set(stopwords)
    emptyFiles = []

    # sparse matrix representation: the coefficient
    # with coordinates (rows[i], cols[i]) contains value data[i]
    rows, cols, data = [], [], []

    # iterate through the local html files
    for num in range(1, totalDocuments):
        stringNum = str(num)
        if 100 > num > 9:
            stringNum = "0" + stringNum
        elif num < 10:
            stringNum = "00" + stringNum

        rows.append(num)

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

    for word in frequencyTokens:
        cols.append(word)
        inverseDocumentFreq[word] = math.log(totalDocuments / float(frequencyTokens[word]))

    weightArray = []
    weightDocPair = {}

    # Average of each tfidf by word and average cosine similarity

    # We know the the order of the frequencyTokens are the same
    for num in range(1, totalDocuments):
        weightDocPair[num] = []
        if num in emptyFiles:
            pass
        else:
            # allTermFrequency[num]
            termFreq = frequencyTokens
            # for all the words in frequencyTokens in the current document, save word weight if it exists
            for word in termFreq:
                # for each term, calculate the weight of each word by tf-idf and save to the array if it exists
                if word not in allTermFrequency[num]:
                    weightDocPair[num].append(0)
                else:
                    weightDocPair[num].append((termFreq[word] * inverseDocumentFreq[word]))
        weightArray.append(weightDocPair[num])

    numpyArray = np.array(weightArray)
    sparseMartix = sparse.csr_matrix(numpyArray)

    similarities = cosine_similarity(sparseMartix)

    cluster = AgglomerativeClustering(n_clusters=1, affinity='cosine', linkage='single').fit(similarities)

    # print(cluster.labels_)

    # visualize cluster in a scatter plot
    plt.figure(figsize=(50, 50))
    dend = shc.dendrogram(shc.linkage(similarities, method='single'))
    # plt.scatter(similarities[:, 0], similarities[:, 1], c=cluster.labels_, cmap='rainbow')
    # centroid = shc.dendrogram(shc.centroid(similarities))
    plt.show()

    endTime = time.time()
    seconds = endTime - startTime
    print('trial: ' + str(seconds) + ' seconds')
