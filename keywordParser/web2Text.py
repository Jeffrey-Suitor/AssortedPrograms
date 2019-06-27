# Libraries {{{
import urllib.request
import bs4
import re
import os
import logging as log
# }}}


# replace {{{
def replace(string, substitutions):

    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)
# }}}


# getTitle {{{
def getTitle(soup):
    substitutions = {r"\r": "",
                     r"\t": "",
                     r"\n": "",
                     }
    try:
        parse = soup.find('title')
        unformattedTitle = parse.renderContents().decode().split("|", 1)[0]
        title = replace(unformattedTitle, substitutions).strip()
        return title
    except AttributeError:
        return False

# }}}


# generateReports {{{
def generateReports(urlFile, directoryName, filePrefix, newGen):

    # Create a list of the websites
    with open(urlFile) as websites:
        websiteList = websites.read().split()

    currentEntry = len(websiteList) - 1
    for i in range(len(websiteList)):
        # Iterate backwards through list so only new entries are added
        url = str(websiteList[currentEntry - i])
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers=headers)
        webpage = str(urllib.request.urlopen(req).read())
        soup = bs4.BeautifulSoup(webpage, "lxml")
        title = getTitle(soup)
        visibleText = soup.getText()  # Get the text from the document
        newString = re.sub("[^a-zA-Z]+", " ",  # Substitue non standard characters
                           str(visibleText.encode("utf-8")))
        if title:
            reportName = ''.join([directoryName, '/', title, ".txt"])
        else:
            reportName = ''.join(
                [directoryName, '/', filePrefix, str(i+1), ".txt"])
            log.info("No title found. Naming file {0}".format(reportName))

        if newGen:
            print("{} urls to scan".format(len(websiteList)-i))
            if os.path.isfile(reportName):
                log.warning("Entry {0} is a duplicate.".format(i))

            else:  # If file does not exist
                # Create new report
                with open(reportName, "w+") as newReport:
                    newReport.write(newString)
                    log.info("Creating {}".format(reportName))

        else:
            if not os.path.isfile(reportName):  # If file does not exist
                print("Adding new entry {}".format(i+1))
                # Create new report
                with open(reportName, "w+") as newReport:
                    newReport.write(newString)
                    log.info("Creating {}".format(reportName))
            else:
                print("New entries exhausted")
                log.info("{} file found".format(reportName))
                return True

    log.info("All urls have been written")
    # }}}
