from scrap import twitter_query,getinfo
from pdf import keywords, readpdf
from json2html import *
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template,send_file
from werkzeug.utils import secure_filename
from IPython.display import HTML
import base64
from io import BytesIO
#twitter_query(keywords(readpdf(),5))

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('index.html', error='No file uploaded!',keywords='keywords')
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],'pdf.pdf'))
            return render_template('index.html', keywords=keywords(readpdf(),20))
        else:
            return render_template('index.html', error='Please upload a PDF file',keywords='keywords')
    return render_template('index.html', keywords='keywords')

@app.route('/scrap', methods=['GET', 'POST'])
def scraper():
    if request.method=='POST':
        q= str(request.form.get('keywords'))
        h=str(request.form.get('hashtags'))
        u=str(request.form.get('uid'))
        return redirect(('/table/{}'.format(q+"%20"+u+"%20"+h)))
    return render_template('scrap.html') 

@app.route('/table/<query>', methods=['GET', 'POST'])
def table(query):
    if request.method=='POST':
        s=str(request.form.get('Sentiment'))
        df,pos,neg,neu= twitter_query(query)
        #fig = sentplot(df)
        df=df.iloc[:,:]
        if(s!='All'):
            df = df[df['sentiment'] == s] 
        colnames=tuple(list(df.columns.values))
        rows=list(df.itertuples(index=False))     
        return render_template('table.html', headings=colnames, data=rows,pos=pos,neg=neg,neu=neu) 
    df,pos,neg,neu= twitter_query(query)
    #fig = sentplot(df)
    df=df.iloc[:,:]
    colnames=tuple(list(df.columns.values))
    rows=list(df.itertuples(index=False))
    return render_template('table.html', headings=colnames, data=rows,pos=pos,neg=neg,neu=neu) 

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    try:
        json=getinfo(name)
    except:
        return 'User not found'
    return render_template('userinfo.html',
                           name=json['name'], 
                           imageurl=json['profile_image_url_https'], 
                           fcount=json['followers_count'], 
                           sname=json['screen_name'], 
                           fav=json['favourites_count'], 
                           friends=json['friends_count'],
                           verified=json['verified'],
                           date=json['created_at'],
                           description=json['description']
                           ) 

@app.route('/usersearch', methods=['GET', 'POST'])
def usersearch():
    if request.method=='POST':
        u=str(request.form.get('uid'))
        return redirect(('/user/{}'.format(u)))
    return render_template('usersearch.html') 
if __name__ == '__main__':
   app.run(debug = True)