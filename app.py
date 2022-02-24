from flask import Flask, render_template, request, send_file, session, redirect, flash, send_from_directory
import os
from pdf_to_audio_book import pdf_to_audio


app = Flask(__name__)


app.secret_key = 'super-secret-key'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = 'D:\\codefiles\\python project\\pdf-2-audio-in-flask\\static\\pdf\\'


@app.route('/')
def home():
    link = "/converter"
    return render_template('index.html', link=link)


@app.route('/converter')
def converter():
    return render_template('converter.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if(request.method == 'POST'):
        f = request.files['file1']
        start = request.form.get('start')
        end = request.form.get('end')
        session['pdfname'] = str(f.filename)
        session['start']= int(start)
        session['end']= int(end)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'] + f.filename))
    return redirect('/down')


@app.route('/downloadFile/<string:path>', methods = ['GET', 'POST'])
def downloadFile(path):
    file = session['audio_name']
    path  = file
    directory = "D:\\codefiles\\python project\\pdf-2-audio-in-flask\\static\\audio\\" + path
    return send_file(directory, as_attachment=True)

@app.route('/down', methods = ['GET', 'POST'])
def download():
    try:
        name = session['pdfname']
        s = session['start']
        e = session['end']
        pdf_name = 'D:\\codefiles\\python project\\pdf-2-audio-in-flask\\static\\pdf\\' + session['pdfname']
        main_name = pdf_to_audio(pdf_name, s, e)
        session['audio_name'] = main_name
        return render_template('download.html',  name=name, main_name=main_name)
    except Exception as e:
        return render_template('error.html', error=(str(e)))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorfourzerofour.html')


@app.route('/PrivacyPolicy')
def PrivacyPolicy():
    return render_template('PrivacyPolicy.html')

if __name__ == "__main__":
    app.run(debug=True)