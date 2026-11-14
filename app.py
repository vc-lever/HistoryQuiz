import flask
import logging
import sys
import json
from threading import Lock
import os
from transform_json import transform
DATA_FILE = "data/questions.json"

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

application = flask.Flask(__name__)
lock = Lock()

os.makedirs('data', exist_ok=True)

@application.route('/')
def home():
    return flask.render_template('submit.html')

@application.route('/about')
def about():
     return "History quiz"

@application.route('/teacher')
def teacher():
     return flask.render_template('teacher.html')

@application.route('/api/submit', methods=['POST'])
def on_submit():
    payload = flask.request.get_json(silent=True)
    if not isinstance(payload, dict):
        return flask.jsonify(status=400, error='Request body must be a JSON object.'), 400

    logging.info('Received quiz submission')
    logging.info(payload)
    transformed_form = transform(payload)
    with lock:
        try:
            with open(DATA_FILE) as f:
                questions = json.load(f)
        except:
                questions = []
        questions += transformed_form

        with open(DATA_FILE, "w") as f:
             json.dump(questions, f, indent=4)

    return flask.jsonify(status=200, error=None), 200

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80, debug=True)
    