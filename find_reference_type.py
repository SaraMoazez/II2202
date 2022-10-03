from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
import re
import os
import pandas as pd


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
        #else:
         #   unclassifiedReferences = open(file[0:17]+".txt", "a", encoding="utf-8")
          #  unclassifiedReferences.write(reference)
           # unclassifiedReferences.write("\n")
            #unclassifiedReferences.close()

    diva_df=pd.read_excel(open("eecs-2022with_references_info_kopia.xlsx", 'rb'))
    for idx, row in diva_df.iterrows():
        #print(row["PID"])
        print(row["PID"], file[0:7])
        if str(row["PID"]) == str(file[0:7]):
            print(row["PID"])
            diva_df.loc[idx, 'Number of Journals'] = journal
            diva_df.loc[idx, 'Number of Books'] = isbn
            diva_df.loc[idx, 'Number of Conference Papers'] = conference
            diva_df.loc[idx, 'Number of Websites'] = webPage
            diva_df.loc[idx, 'Number of References'] = (len(splitText)-1)

    #print("Total references: ", (len(splitText)-1), "Number of unclassified references: ", ((len(splitText)-1)-(journal+conference+isbn+webPage)))
    #print("occurrences of journal: " , journal , "occurrences of isbn: " , isbn, "occurrences of conference: ", conference, 
     #       "occurrences of webpages: " , webPage)

    writer = pd.ExcelWriter("eecs-2022with_references_info_kopia.xlsx", engine='xlsxwriter')
    diva_df.to_excel(writer, sheet_name='ReferencesInfo')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


files = os.listdir("./dataset")
for file in files:
    get_reference_types(file)