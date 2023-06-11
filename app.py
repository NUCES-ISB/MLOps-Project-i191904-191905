from flask import Flask, redirect, request, render_template
import pickle
import os
from sklearn.neighbors import KNeighborsClassifier
import pickle

ROOT_PATH = os.getcwd()
app = Flask(__name__)
try:
    model = pickle.load(open(ROOT_PATH + '/knn_model.sav', 'rb'))
except:
    print(f"Model unable to be loaded from location {ROOT_PATH + '/knn_model.sav'}")
    model = None
labels = {0: 'normal', 1: 'erroroneous', 2: 'probably a DDoS attack', 3: 'probably a data probe',
          4: 'probably a scan attack', 5: 'probably a man-in-the-middle-attack'}


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.route('/', methods=['GET', 'POST'])
def home():
    global model
    if request.method == "POST":
        if model == None:
            try:
                model = pickle.load(open(ROOT_PATH + '/knn_model.sav', 'rb'))
            except:
                message = 'unable to be determined, as model is missing'
                return render_template('home.html', message=message, invalid=message)
        input_string = request.form['input_string']
        if len(input_string.split(',')) == 13:
            try:
                num_label = model.predict(
                    [[float(x) for x in input_string.split(',')]])[0]
                message = labels[num_label]
            except:
                message = 'unable to be determined, as input data seems invalid.'
                return render_template('home.html', message=message, invalid=message)
        else:
            message = 'unable to be determined, as input data seems invalid.'
            return render_template('home.html', message=message, invalid=message)
        if num_label == 0:
            return render_template('home.html', message=message)
        else:
            return render_template('home.html', message=message, danger=message)
    return render_template('home.html')