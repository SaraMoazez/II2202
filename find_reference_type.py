from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
import re
import os


def get_reference_types(file):
    pdfFileObj = open("./dataset/"+file,'rb')

    reader = PdfReader(pdfFileObj)

    output = ""
    for i in range(reader.numPages):
        pageObj = reader.getPage(i)
        output += pageObj.extractText()

    #print(output)
    pattern = r'\[[0-9]+\]'
    splitText = re.split(pattern, output)
    #print(len(splitText))

    volumeNumber = r'[0-9]+\.+[0-9]'
    volumeNumberWithParantheses = r'[0-9]+\(+(?<!\d)\d{1,3}(?!\d)+\)'
    url = r'(http(s)?)|(www)'
    webPage = 0
    journal = 0
    isbn = 0
    conference = 0
    for reference in splitText:
        #print(reference)
        if ("journal" in reference or "Journal" in reference or "no." in reference or re.search(volumeNumber, reference)
        or re.search(volumeNumberWithParantheses, reference) or "ISBN" in reference or "conference" in reference
        or "Conference" in reference or "symposium" in reference or "Symposium" in reference 
        or ("Accessed" in reference and re.search(url, reference))):
            if "ISBN" in reference:
                isbn += 1
            elif  ("conference" in reference or "Conference" in reference or "symposium" in reference or "Symposium" in reference):
                conference += 1
            elif ("Accessed" in reference and re.search(url, reference)):
                webPage += 1
            else:
                journal += 1
        else:
            unclassifiedReferences = open(file[0:17]+".txt", "a", encoding="utf-8")
            unclassifiedReferences.write(reference)
            unclassifiedReferences.write("\n")
            unclassifiedReferences.close()

    print("Total references: ", (len(splitText)-1), "Number of unclassified references: ", ((len(splitText)-1)-(journal+conference+isbn+webPage)))
    print("occurrences of journal: " , journal , "occurrences of isbn: " , isbn, "occurrences of conference: ", conference, 
            "occurrences of webpages: " , webPage)

files = os.listdir("./dataset")
for file in files:
    get_reference_types(file)