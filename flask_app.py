from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import re
import os
import librosa
from werkzeug.utils import secure_filename
from drum_annotation import DrumAnnotation

UPLOAD_FOLDER = "./static/uploads"
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
annotator = DrumAnnotation("./trained_models/nov26.pkl")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/song/<filename>')
def display_drum(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    song, sr = librosa.core.load(path)
    return render_template("music.html", file_name=url_for('static', filename=os.path.join('uploads', filename)),
                           drum_events=annotator.get_drum_prediction_times(song, sr))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('display_drum', filename=filename))
    return render_template("upload.html")


@app.route('/testing')
def get_test():
    path = "./static/test_data/fort_minor-remember_the_name_127-145/"
    file = 'test_data/fort_minor-remember_the_name_127-145/fort_minor-remember_the_name_127-145_with_effects.wav'
    drum_types = {"Snare drum", "Bass drum"}
    drum_events = {}
    for drum in drum_types:
        with open(path + drum + ".txt", "r") as annotation:
            times = []
            for line in annotation:
                times.append(float(re.findall("\d+\.\d+", line)[0]))
            drum_events[drum] = times
            annotation.close()
    print(drum_events)
    return render_template("music.html", file_name=url_for('static', filename=file), drum_events=drum_events)

@app.route('/export', methods=['POST'])
def export_data():
    '''
    Receive the drum events and some meta data as a POST
    Build the output around these
    '''
    print(request.form) # get the form items
    print(request.data) # get the attached times
    return send_file('./static/uploads/test.txt', as_attachment=True)