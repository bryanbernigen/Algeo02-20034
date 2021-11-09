from flask import Flask, render_template,redirect,url_for,request, current_app
import secrets,os
from PIL import Image
from werkzeug.utils import secure_filename

from forms import PostForm

import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def home():
    form = PostForm()
    return render_template('index.html',title='Upload', form=form)

@app.route('/upload', methods=['GET','POST'])
def upload():
    form = PostForm()
    print("a",form.validate())
    if (request.method == "POST" and form.validate()):
        scale = form.scale.data
        print("masuk",scale)
        fileName=secure_filename(form.picture.data.filename)
        form.picture.data.save('uploads/'+fileName)
        print(fileName)

        return redirect(url_for('upload', form=form, fileName=fileName))
    return render_template('upload.html', form=form)

