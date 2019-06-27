# Libraries {{{
import web2Text
import pdf2Text
from setup import *
import os
import shutil
from os import listdir
from os.path import isfile, join
import time
# }}}


# generateAlphabet {{{
def generateAlphabet():
    # Create alphabet list
    return [chr(letter) for letter in range(97, 123)]
# }}}


# createTextFileList {{{
def createTextFileList(TEXTFILE):
    # Get a list of all words in the TEXTFILE
    with open(TEXTFILE, 'r') as file:
        return file.read().split()
# }}}


# keywordSorter {{{
def keywordSorter(KEYWORDFILE):
    # Create sorted keyword list

    keywordList = createTextFileList(KEYWORDFILE)
    keywordList.sort()  # Sort to increase effiency

    alphabet = generateAlphabet()

    sortedKeywordList = [[] for x in range(26)]
    # Create a 2d array with 26 elements

    for i in range(len(keywordList)):  # The keyword list
        for k in range(len(alphabet)):  # The alphabet list
            # Sort each keyword by first letter
            if keywordList[i][0].lower() == alphabet[k]:
                sortedKeywordList[k].append(keywordList[i].lower())
                break

    return sortedKeywordList  # Return the sorted list
# }}}


# reportSorter {{{
def reportSorter(REPORTFILE, KEYWORDLIST):

    reportList = createTextFileList(REPORTFILE)
    reportList.sort()

    shortestString, longestString = stringLengthFinder(KEYWORDLIST)

    alphabet = generateAlphabet()

    sortedReportList = [[] for x in range(26)]

    for i in range(len(reportList)):
        for k in range(len(alphabet)):
            if shortestString <= len(reportList[i]) <= longestString:
                # If word is between shortest and longest inclusive
                if reportList[i][0].lower() == alphabet[k]:
                    sortedReportList[k].append(reportList[i])
                    break

    return sortedReportList
# }}}


# keyWordTest {{{
def keywordTest(REPORTLIST, KEYWORDLIST):
    flatREPORTLIST = [word for letter in REPORTLIST for word in letter]
    flatKEYWORDLIST = [word for letter in KEYWORDLIST for word in letter]
    for i in range(len(flatREPORTLIST)):
        for k in range(len(flatKEYWORDLIST)):
            if flatREPORTLIST[i].lower() == flatKEYWORDLIST[k].lower():
                # If keyword matches lowercase
                return True
# }}}


# stringLengthFinder {{{
def stringLengthFinder(KEYWORDLIST):
    shortestString = 100  # placeholder for the shortest string
    longestString = 0  # placeholder for the longest string
    for letter in range(len(KEYWORDLIST)):
        for word in range(len(KEYWORDLIST[letter])):

            if len(KEYWORDLIST[letter][word]) < shortestString:
                # If the keyword is shorter than shortest
                shortestString = len(KEYWORDLIST[letter][word])

            if len(KEYWORDLIST[letter][word]) >= longestString:
                # If the keyword is longer than longest
                longestString = len(KEYWORDLIST[letter][word])

    return shortestString, longestString
# }}}


# userInput {{{
def userInput():
    newParse = None
    while newParse not in ('y', 'Y', 'n', 'N'):

        newParse = input('Use currently generated reports? Y/N : ')

        if newParse == 'y' or newParse == 'Y':  # Use currently generated reports
            log.info("Using currently generated reports")
            startTime = time.time()
            return startTime, False  # Record the start time

        elif newParse == 'n' or newParse == 'N':  # Generate new reports
            log.info("Generating new reports")
            startTime = time.time()  # Record the start time

            try:
                shutil.rmtree(dirName)  # Remove old directory
                os.makedirs(dirName)  # Make new directory
                return startTime, True

            except FileNotFoundError:  # If no directory exists
                os.makedirs(dirName)  # Make new directory
                return startTime, True

        else:
            print('This is not a valid selection')

            # }}}


# main {{{
def main():

    if os.path.isfile(infoFile):
        os.remove(infoFile)  # Delete the old info file

    # Initial setup
    startTime, regen = userInput()  # Get the start time
    srtKWList = keywordSorter(keywordFile)  # Sort the keywords

    # Generate the reports from the file links
    print("Starting url scanning")
    web2Text.generateReports(urlFile, dirName, filePrefix, regen)
    print("Url scanning complete\nStarting pdf scanning")
    pdf2Text.pdf2Text(dirName, pdfPath)

    filePath = []
    fileNames = []
    for file in listdir(dirName):
        if isfile(join(dirName, file)):
            filePath.append(''.join([dirName, '/', file]))
            fileNames.append(file)
    filePath.sort()
    fileNames.sort()

    # Main Loop
    i = 0
    for filename in filePath:

        srtRPList = reportSorter(filename, srtKWList)

        if keywordTest(srtRPList, srtKWList):
            with open(infoFile, "a+") as f:
                f.write("Title : {0}\n".format(filename.split("/")[1]))
                f.write("\t{0:20s}{1}\n".format("Keywords", "Instances"))
                for ltr in range(26):
                    for kWord in (range(len(srtKWList[ltr]))):
                        instances = 0
                        for rWord in range(len(srtRPList[ltr])):
                            if srtKWList[ltr][kWord] == srtRPList[ltr][rWord]:
                                instances += 1
                        if instances != 0:
                            f.write("\t{0:20s}{1}\n"
                                    .format(srtKWList[ltr][kWord], instances))
                f.write('{:-<40}\n\n\n'.format(""))

    finalTime = time.time()-startTime
    print("Reports generated in {0} seconds.".format(round(finalTime, 2)))
    print("Your output file is {}".format(infoFile))

    # }}}
