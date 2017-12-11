# CSC 475 Final Project

Shae Brown & Jarred Hawkins

See our [written report](report_final.pdf) for more technical info.

A live demo based off of the deploy branch is available [here](https://drum-annotation.herokuapp.com/).

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

Right now there is no way to do this using the front end. You may retrain the model by running the *train.py* file. This file retrains a model using the data in *static/test_data*.

The format of the training data is as follows:

File structure:

```txt
static/test_data
├── song1_name
│   ├── Bass drum.txt
│   ├── song1.wav
│   ├── Chinese ride cymbal.txt
│   ├── Hi-hat closed.txt
│   ├── Hi-hat open.txt
│   ├── Low tom.txt
│   └── Snare drum.txt
└── song2_name
    ├── Bass drum.txt
    ├── song2.mp3
    ├── Hi-hat closed.txt
    ├── Hi-hat open.txt
    └── Snare drum.txt
```

Annotation file structure example:

_Note: Class names in this file are optional. You may use a list of times separated by newlines as well._

```txt
0.773469387   bd
2.537142857   bd
4.323129251   bd
6.106122448   bd
7.866303854   bd
9.659297052   bd
11.426757369   bd
13.219863945   bd
```

Once *train.py* is run, you can change the model file in the header of *flask_app.py*

## Exporting data

Using the export feature on the main window, you can output the file in the desired formats. Using python style string formatting you may also change the format of these output lines and file names.

Once the annotated data is exported, you may also move it into the the training folder and retrain the model using your annotated data.

## Included data sets

Our initial model was trained with several data sets. These data sets are as follows:

- [MDB DRUMS – AN ANNOTATED SUBSET OF MEDLEYDB FOR AUTOMATIC DRUM TRANSCRIPTION](https://github.com/CarlSouthall/MDBDrums)
- [DREANSS: DRum Event ANnotations for Source Separation](https://www.upf.edu/web/mtg/dreanss)

Due to licensing issues, we can not redistribute the data set along with this repository. We hope that these links will provide a starting point to anyone wishing to build their own models.