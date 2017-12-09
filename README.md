# CSC 475 Final Project

Shae Brown & Jarred Hawkins

See our [written report](TODO.pdf) for more technical info.

## Installation

Install all the dependencies in the project using your package manager of choice. For pip users this will be `pip install -r requirements.txt`

Then run the app using:
```bash
flask run
```

## Using the program

Once the app is running, open the flask webpage (defaults to *127.0.0.1:5000*).

This will prompt you to upload an audio file. Currently *.wav* and *.mp3* files are supported.

Once you upload a file it will redirect to the annotation editing page. This page allows you to:

- create new drum events by double clicking the canvas
- edit current event times by dragging and dropping the circle
- changing/deleting classes by right clicking the events

## Retraining the model

Right now there is no way to do this using the front end. You may retrain the model by running the *train.py* file. This file retrains a model using the data in *static/test_data*. See that folders README for a description of the training data format.

Once *train.py* is run, you can change the model file in the header of *flask_app.py*

## Exporting data

Using the export feature on the main window, you can output the file in the desired formats. Using python style string formatting you may also change the format of these output lines and file names.

Once the annotated data is exported, you may also move it into the the training folder and retrain the model using your annotated data.