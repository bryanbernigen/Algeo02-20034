from flask import Flask, render_template,redirect,url_for,request, current_app
import secrets,os
from PIL import Image
from werkzeug.utils import secure_filename, send_file, send_from_directory


from imageRead import imageRead
from forms import PostForm

import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/',methods=['POST', 'GET'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PostForm()
    print("a",form.validate_on_submit())
    scale = form.scale.data
    print(request.form)
    filePath=''
    imgJadi =''
    waktu=0
    if(form.validate_on_submit() and request.method == 'POST'):
        fileName=secure_filename(form.picture.data.filename)
        form.picture.data.save('static/uploads/'+fileName)
        print(fileName)
        print("masuk",scale)
        filePath = "/uploads/"+fileName
        print(filePath)
        imgJadi, waktu = imageRead('static'+filePath,scale/100)

    #return redirect(url_for('upload',))
    return render_template('upload.html', form=form, imgJadi=imgJadi, waktu=waktu, filePath=filePath)

if __name__ == '__main__':
    app.run(debug=True)