from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
import re

pdfFileObj = open("./dataset/1534466-FULLTEXT01-refpages.pdf",'rb')

reader = PdfReader(pdfFileObj)

output = ""
for i in range(reader.numPages):
    pageObj = reader.getPage(i)
    output += pageObj.extractText()

#print(output)
pattern = r'[+[0-9]+]'
splitText = re.split(pattern, output)
#print(len(splitText))

volumeNumber = r'[0-9]+\.+[0-9]'
volumeNumberWithParantheses = r'[0-9]+\(+(?<!\d)\d{1,3}(?!\d)+\)'
journal = 0
isbn = 0
conference = 0
for reference in splitText:
    if ("journal" in reference or "Journal" in reference or "no." in reference or re.search(volumeNumber, reference)
     or re.search(volumeNumberWithParantheses, reference) or "ISBN" in reference or "conference" in reference
     or "Conference" in reference or "symposium" in reference or "Symposium" in reference):
        if "ISBN" in reference:
            isbn += 1
        elif  ("conference" in reference or "Conference" in reference or "symposium" in reference or "Symposium" in reference):
            conference += 1
        else:
            journal += 1
print("occurrences of journal: " , journal , "occurrences of isbn: " , isbn, "occurrences of conference: ", conference)