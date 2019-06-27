import glob
import PyPDF2
import textract
import os
import logging as log


def pdf2Text(dirName, path):
    i = 0
    files = glob.glob(path)  # Get all files
    for name in files:
        print("{} pdfs to scan".format(len(files)-i))
        i += 1
        nameList = name.split(os.sep)
        reportName = ''.join([dirName, '/', nameList[-1], ".txt"])
        if not os.path.isfile(reportName):  # If the file doesn't exist
            with open(name, 'rb') as f:
                pdfReader = PyPDF2.PdfFileReader(f, strict=False)

                # Get the text
                num_pages = pdfReader.numPages
                count = 0
                text = ""
                while count < num_pages:
                    pageObj = pdfReader.getPage(count)
                    count += 1
                    text += pageObj.extractText()
                if text != "":
                    text = text
                else:
                    text = textract.process(
                        name, method='tesseract', language='eng')

                punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                noPunct = ""
                for char in text:
                    if char not in punctuations:
                        noPunct = noPunct + char

                else:
                    with open(reportName, "w+") as newReport:
                        newReport.write(noPunct)
                        log.info("Writing {}".format(reportName))
        else:
            log.info("{} already exists".format(reportName))
