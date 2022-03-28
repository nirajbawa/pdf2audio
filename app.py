import json
from logging import exception
from pyexpat.errors import messages
import weakref
from flask import Flask, render_template, request, send_file, session, redirect, flash, send_from_directory, jsonify
import os
from text_to_audio_book import pdf_to_audio
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from pdf_to_image_to_text import covert_pdf_to_image
from threading import Timer
import random
import shutil
# import redis
import time
# from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process
from deletingmod import deletingdic
from onlypdftoimage import covert_pdffile_to_image

with open('app_config.json', 'r') as configData:
    params = json.load(configData)["params"]


  


app = Flask(__name__)

# r = redis.Redis()

app.secret_key = 'super^-&web&-k&ey'
ALLOWED_EXTENSIONS = set(['pdf'])
app.config['PDF_UPLOAD_FOLDER'] = params["pdf_upload_folder_local"]
app.config['AUDIO_PATH'] = params["audio_upload_local"]
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024


  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# app.app_context().push()
# def timeoutfunc(dname):
#     print("stating deleting")
#     shutil.rmtree(dname)
    
# dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']
# timeoutfunc(dname)

@app.route('/')
def home():
    link = "/converter"
    return render_template('home.html', link=link)

@app.route('/converter/<string:typeofcon>')
def converter(typeofcon):
    try:
        if(typeofcon=="pdftoaudio"):
            message = "make sure your file is less then 300MB"
            converter = "/uploader"
            return render_template('converter.html', message=message, upurl  = converter)
        elif(typeofcon=="pdftotext"):
            message = "make sure your file is less then 300MB"
            converter = "/uploaderforimageandtext/pdftotext"
            return render_template('converter.html', message=message, upurl  = converter)
        elif(typeofcon=="pdftoimage"):
            title = "pdf to image"
            urlcon = "pdftoimage"
            message = "make sure your file is less then 300MB"
            return render_template('pdftoimage.html', message=message, title=title, urlcon=urlcon)
        else:
            return redirect("/")
    except Exception as error:
        return redirect("/")


@app.route('/uploaderforimageandtext/<string:typeofcon>', methods = ['GET', 'POST'])
def uploaderforimagandtext(typeofcon):
    if(request.method == 'POST'):
        try:
            if 'file1' not in request.files:
                return redirect("/pdftoaudio/" + typeofcon)

            # getting pdf from user 
            try:

                f = request.files['file1']
                start = request.form.get('start')
                end = request.form.get('end')
                pdflang = request.form.get('lagpann')
            except  Exception as geterror : 
                return redirect("/pdftoaudio/" + typeofcon)

            # checking file error

            if f.filename == '':
                return redirect("/pdftoaudio/" + typeofcon)

            filename = secure_filename(f.filename)

            if f and allowed_file(filename):
                #sending pdf to audio converting configration in session
                try:
                    session['pdfname'] = str(filename)
                    session['start']= int(start)
                    session['end']= int(end)
                    session['pdflangu'] = pdflang
            

                    #creating folder for current pdf
                    randintnum = random.randint(1,1000)
                    directname = os.path.splitext(filename)[0] + str(randintnum)
                    
               
                    session['dname'] = directname
                    
                    makenewdirect = app.config['PDF_UPLOAD_FOLDER'] + directname 
                    os.mkdir(makenewdirect)
                 
                    fullpathofpdf = app.config['PDF_UPLOAD_FOLDER'] + directname + '\\'
                    #add path in session
                    session["pdfpath"] = fullpathofpdf
                    
                    session["contype"] = typeofcon

                    #upload it on this path
                    f.save(os.path.join(app.config['PDF_UPLOAD_FOLDER'] + directname + '\\' + filename))
                    
                    
                    return redirect('/download')

                except RequestEntityTooLarge as errorlog:
                    message = "your file size greater thrn 300MB we can't converte it"
                    redirect("/pdftoaudio/" + typeofcon)
            else:
                return redirect("/pdftoaudio/" + typeofcon)

        except Exception as o:
            return redirect("/pdftoaudio/" + typeofcon)



@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if(request.method == 'POST'):
        try:
            if 'file1' not in request.files:
                return redirect("/converter")

            # getting pdf from user 
            try:

                f = request.files['file1']
                start = request.form.get('start')
                end = request.form.get('end')
                pdflang = request.form.get('lagpann')
            except  Exception as geterror : 
                return redirect('/converter')

            # checking file error

            if f.filename == '':
                return redirect("/converter")

            filename = secure_filename(f.filename)

            if f and allowed_file(filename):
                #sending pdf to audio converting configration in session
                try:
                    session['pdfname'] = str(filename)
                    session['start']= int(start)
                    session['end']= int(end)
                    session['pdflangu'] = pdflang
                 

                    #creating folder for current pdf
                    randintnum = random.randint(1,1000)
                    directname = os.path.splitext(filename)[0] + str(randintnum)
                    
               
                    session['dname'] = directname
                    
                    makenewdirect = app.config['PDF_UPLOAD_FOLDER'] + directname 
                    os.mkdir(makenewdirect)
                 
                    fullpathofpdf = app.config['PDF_UPLOAD_FOLDER'] + directname + '\\'
                    #add path in session
                    session["pdfpath"] = fullpathofpdf

                    #upload it on this path
                    f.save(os.path.join(app.config['PDF_UPLOAD_FOLDER'] + directname + '\\' + filename))
                    return redirect('/down')

                except RequestEntityTooLarge as errorlog:
                    message = "your file size greater thrn 300MB we can't converte it"
                    return redirect('/converter', message=message)
            else:
                return redirect('/converter')

        except Exception as o:
            redirect('/converter')



@app.route('/downloadFile/<string:path>', methods = ['GET', 'POST'])
def downloadFile(path):
    try:
        #getting audio file for download
        #file name form download path in session
        file = session['audio_name']
        audiopath = session["pdfpath"] + 'audio\\' + file
        #connecting file path of audo file for download
        directory = os.path.join(audiopath)
        return send_file(directory, as_attachment=True)
    except Exception as error:
        return redirect('/')


@app.route('/downloadimageortext/<string:filename>', methods = ['GET', 'POST'])
def downloadtoimage(filename):
    try:
        #getting audio file for download
        #file name form download path in session
        filepath = session["pdfpath"] + 'image\\' + filename
        #connecting file path of audo file for download
        directory = os.path.join(filepath)
        return send_file(directory, as_attachment=True)
    except Exception as error:
        return redirect('/')


@app.route('/downloadtotext/<string:filename>', methods = ['GET', 'POST'])
def downloadtotext(filename):
    try:
        #getting audio file for download
        #file name form download path in session
        filepath = session["pdfpath"] + 'text\\' + filename
        #connecting file path of audo file for download
        directory = os.path.join(filepath)
        return send_file(directory, as_attachment=True)
    except Exception as error:
        return redirect('/')

@app.route('/download', methods = ['GET', 'POST'])
def downloadforrimgandtext():
    try:

        checkytype =session["contype"]
        
        if(checkytype=="pdftoimage"):
            try:
                #pdf to audio convertion configration session form upload path
                name = session['pdfname']
                s = session['start']
                e = session['end']
                fullpath = session["pdfpath"]

                #storing upload folder path for sending for converting pdf to audio
                pdf_name = fullpath + name
                #call audio to pdf function form pdf_to_audio_book.py
                #give him to pdf name , start form page, end from page, and audio file storing path
                dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']

                imagefile = covert_pdffile_to_image(pdf_name, s, e, fullpath)
                session['text_file'] = imagefile
                dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']
                begin = processClass(dname)
                return render_template('downloadimgandtext.html',  name=name, main_name = imagefile)
            except Exception as a:
                return redirect("/")


        elif(checkytype=="pdftotext"):
            try:
                name = session['pdfname']
                s = session['start']
                e = session['end']
                fullpath = session["pdfpath"]
                pdflang = session['pdflangu']
                pdflangcheck = ""
                pdflangforaudio = ""

                #condition for image lang
                if(pdflang=="marathi" or pdflang=="hindi"):
                    pdflangcheck = "Devanagari"
                elif(pdflang=="english"):
                    pdflangcheck = "eng"
                else:
                    pdflangcheck = "eng"
             
                #storing upload folder path for sending for converting pdf to audio
                pdf_name = fullpath + name
                #call audio to pdf function form pdf_to_audio_book.py
                #give him to pdf name , start form page, end from page, and audio file storing path
                dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']

                textfile = covert_pdf_to_image(pdf_name, s, e, fullpath, pdflangcheck)

                session['text_file'] = textfile
            
                dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']
                foldname = session['dname']
                
                begin = processClass(dname)
    

                #sending audio file name, file name to download page
                return render_template('downloadtext.html',  name=name, main_name = textfile)
            except Exception as error:
                return redirect("/")

    except Exception as e:
        return redirect("/")


@app.route('/down', methods = ['GET', 'POST'])
def download():
    try:
        #pdf to audio convertion configration session form upload path
        name = session['pdfname']
        s = session['start']
        e = session['end']
        fullpath = session["pdfpath"]
        pdflang = session['pdflangu']
        pdflangcheck = ""
        pdflangforaudio = ""

        #condition for image lang
        if(pdflang=="marathi" or pdflang=="hindi"):
            pdflangcheck = "Devanagari"
        elif(pdflang=="english"):
            pdflangcheck = "eng"
        else:
            pdflangcheck = "eng"

        #condition for audio lang
        if(pdflang=="hindi"):
            pdflangforaudio = "hi"
        elif(pdflang=="marathi"):
            pdflangforaudio = "mr"
        elif(pdflang=="english"):
            pdflangforaudio = "en"
        else:
            pdflangforaudio = "en"

        #storing upload folder path for sending for converting pdf to audio
        pdf_name = fullpath + name
        #call audio to pdf function form pdf_to_audio_book.py
        #give him to pdf name , start form page, end from page, and audio file storing path
        dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']

        textfile = covert_pdf_to_image(pdf_name, s, e, fullpath, pdflangcheck)

        session['text_file'] = textfile

        main_name = pdf_to_audio(fullpath+ "text\\" + textfile, fullpath, dname, pdflangforaudio)
        
        session['audio_name'] = main_name
       
        dname = app.config['PDF_UPLOAD_FOLDER'] + session['dname']
        foldname = session['dname']


        begin = processClass(dname)
     
        #sending audio file name, file name to download page
        return render_template('download.html',  name=name, main_name=main_name, foldername=foldname)
    #if pdf is not converting to audio for error handling
    except Exception as e:
        return redirect("/")

@app.route('/offline.html')
def offline():
    error = "your offline"
    return render_template('error.html', error=error)


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


@app.route('/about')
def about():
    return render_template('about.html')

#page not found error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorfourzerofour.html')


@app.route('/PrivacyPolicy')
def PrivacyPolicy():
    return render_template('PrivacyPolicy.html')


class processClass:

    def __init__(self, path):
        self.path = path
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def run(self):

         #
         # This might take several minutes to complete
         time.sleep(60)#second
         deletingdic(self.path) 
        #  

if __name__ == "__main__":
        
    app.run(debug=True, threaded=True)

