from gtts import gTTS 
import PyPDF2
import random

randomnumber = random.randint(1,1000)



def pdf_to_audio(pdf_file_name, page_to_start, page_to_end):

    book = open(pdf_file_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pdftext= ''

    for num in range(page_to_start-1, page_to_end):
        pdftext += pdfReader.getPage(num).extractText()
    myobj = gTTS(text=pdftext, lang='en', slow=False, tld="com")
    filepath = "audio"+str(randomnumber)+".mp3"
    myobj.save("D:\\codefiles\\python project\\pdf-2-audio-in-flask\\static\\audio\\"+ filepath)

    return filepath

  



