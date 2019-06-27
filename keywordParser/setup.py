import textFileRead
import logging as log


'''
Make sure that you have pip3 installed.

If not here is the mac guide as to how:

https://evansdianga.com/install-pip-osx/

Once thats done run pip3 install -r requirements.txt when in this folder

You will also need to download tesseract for mac:
brew install tesseract

To find the location of your the folder in terminal and type pwd
This will give you the full path to the file which you then change in the variables below

Any files that don't exist mean that you have to make your own and change the name appropriately

Variables :

    keywordFile is a file containing each keyword on seperate lines

    urlFile is a file containing links to online files on each lines

    infoFile is the file where the results are outputted to

    dirName is the name of where to save the cleanup files.
        Unless the path is absolute it will create the folder in the current directory

    filePrefix is what to name files that don't have a title

    pdfPath is the path to a folder containing only pdfs
        Make sure to have a * at the end of the path

    Also you will need to run this file as an administrator so that it can do things
'''

# User variables {{{
keywordFile = 'breastCancerDrugs.txt'  # This is your keyword file
urlFile = 'urlLinks.txt'
infoFile = "results.txt"  # This is where the result will be output
dirName = 'reports'  # The directory to store the cleaned files
filePrefix = 'report_'  # What to prefix files that don't have a title with
pdfPath = '/home'  # File to folder with pdfs make sure to have a star on the end
# }}}


if __name__ == '__main__':

    log.basicConfig(level=log.ERROR)
    textFileRead.main()
