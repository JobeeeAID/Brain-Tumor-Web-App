from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import imutils

import numpy as np

from tensorflow import keras
from keras.layers import Dense
from keras.models import load_model
from keras.preprocessing import image
from keras.utils import load_img

# Keras
from PIL import Image, ImageOps

# Loading Model
braintumor_model = load_model('models/vgg19_best5.h5')


# Configuring Flask
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

############################################# BRAIN TUMOR FUNCTIONS ################################################

def model_predict(img_path, model):
    img = keras.utils.load_img(img_path, target_size=(224, 224))
    size = (224, 224)
    imge = ImageOps.fit(img, size, Image.ANTIALIAS)

    imge = imge.convert("RGB")  # Convert to RGB format
    width, height = imge.size

    imge = imge.resize(size)

    img = np.asarray(imge)
    img = cv2.resize(img, dsize=size, interpolation=cv2.INTER_CUBIC)
    img_reshape = img[np.newaxis, ...]
    # img_reshape = img_reshape/255.0
    img_reshape = img.reshape(1, 224, 224, 3)

    prediction = model.predict(img_reshape)
    return prediction

########################### Routing Functions ########################################

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/braintumor')
def brain_tumor():
    return render_template('index.html')




########################### Result Function ########################################





@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        file = request.files['file']
        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            flash('Image successfully uploaded and displayed below')

            pred = model_predict(file_path, braintumor_model)
           

            if pred < 0.5:
                preds = 0
            else:
                preds = 1
            # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour Brain Tumor test results are ready.\nRESULT: {}'.format(firstname,['NEGATIVE','POSITIVE'][pred]))
            return render_template('result.html', filename=filename, fn=firstname, ln=lastname, age=age, r=preds,confidence=int(pred[0][0]*100), gender=gender)

        else:
            flash('Allowed image types are - png, jpg, jpeg')
            return redirect(request.url)



# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    app.run(debug=True)


