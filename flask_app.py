from flask import Flask
from flask import jsonify
from flask import render_template
import re
app = Flask(__name__)

@app.route('/testing')
def get_test():
	path = "./static/test_data/fort_minor-remember_the_name_127-245/"
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