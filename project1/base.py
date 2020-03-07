import codecs, re, time, lxml
from bs4 import BeautifulSoup

if __name__ == '__main__':

    startTime = time.time()
    totalFiles = []
    frequencyTokens = {}
    totalCases = 0
    # iterate through the local html files
    for num in range(1, 503):
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
        localfileDictionary = {}

        specialCheck = re.compile('[@_\[\]#$%^&*()<>/\}{~1234567890-]')

        for word in allWords:
            # Check for special characters that didnt get expunged
            if specialCheck.search(word) is not None:
                # Do nothing
                pass
            # increase to local dictionary if new key or create a new one if it's new, same with the larger dictionary
            elif word in localfileDictionary:
                localfileDictionary[word] = localfileDictionary[word] + 1
                if word in frequencyTokens:
                    frequencyTokens[word] = frequencyTokens[word] + 1
                else:
                    frequencyTokens[word] = 1
            else:
                localfileDictionary[word] = 1
                if word in frequencyTokens:
                    frequencyTokens[word] = frequencyTokens[word] + 1
                else:
                    frequencyTokens[word] = 1
        totalFiles.append(localfileDictionary)
    # removes '' words
    if '' in frequencyTokens:
        frequencyTokens.pop('')

    # create the file of all the tokens sorted by their frequency
    frequencyFile = open("ByFrequencyHW1.txt", "w",  encoding='utf-8', errors='ignore')
    for token in sorted(frequencyTokens.items(), reverse=True, key=lambda x: x[1]):
            frequencyFile.write(str(token[0]) + ": " + str(token[1]) + "\n")
    frequencyFile.close()

    # create the file of all the tokens sorted alphabetically
    alphabeticalFile = open("ByTokenHW1.txt", "w", encoding='utf-8', errors='ignore')
    for token in sorted(frequencyTokens.keys()):
        alphabeticalFile.write(token + ": " + str(frequencyTokens.get(token)) + "\n")
    alphabeticalFile.close()

    # create the file of all the tokens in each html file
    filesFile = open("TokenDocsHW1.txt", "w", encoding='utf-8', errors='ignore')
    fileNum = 1
    for files in totalFiles:
        filesFile.write('File Number:' + str(fileNum) + '\n')
        for token in files:
            filesFile.write(token + ", ")
        filesFile.write('\n----------\n')
        fileNum = fileNum + 1
    filesFile.close()

    endTime = time.time()
    seconds = endTime - startTime
    print('trial: ' + str(seconds) + ' seconds')
