from flask import Flask
from flask import render_template
import re

app = Flask(__name__)

classes = {"Bass drum", "Bongo", "Chinese ride cymbal",
           "Clave", "Cowbell", "Crash cymbal", "Crash cymbal 2",
           "Cross stick", "Hi-hat closed", "Hi-hat open", "Low tom",
           "Lowest tom", "Mid tom", "Ride cymbal", "Shaker", "Snare drum",
           "Snare drum brush", "Snare rim shot", "Splash cymbal", "Tambourine", "Timbala", "Timbala rim shot"}

@app.route('/testing')
def get_test():
    path = "./static/test_data/fort_minor-remember_the_name_127-145/"
    drum_types = {"Snare drum", "Bass drum"}
    drum_events = {}
    for drum in drum_types:
        with open(path + drum + ".txt", "r") as annotation:
            times = []
            for line in annotation:
                times.append(float(re.findall("\d+\.\d+", line)[0]))
            drum_events[drum] = times
            annotation.close()
    return render_template("music.html", drum_events=drum_events)
