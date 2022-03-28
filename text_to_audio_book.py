from gtts import gTTS 
import PyPDF2
import random
import os
import shutil
from threading import Timer


randomnumber = random.randint(1,1000)



def pdf_to_audio(pdf_file_name, audio_save_path, dname, pdflang):

    book = open(pdf_file_name, 'r', encoding="utf8")
    read = book.read()

    myobj = gTTS(text=read, lang=pdflang, slow=False, tld="com")


    filepath = "audio"+str(randomnumber)+".mp3"
    os.mkdir(audio_save_path+'audio\\')
    audiofilepath = audio_save_path + 'audio\\' + filepath
    myobj.save(audiofilepath)
  
   
    return filepath

  



