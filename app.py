import flask
import logging
import sys
import json
from threading import Lock
import os

DATA_FILE = "data/questions.json"

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

application = flask.Flask(__name__)
lock = Lock()

os.makedirs('data', exist_ok=True)

@application.route('/')
def home():
    return flask.render_template('submit.html')



@application.route('/api/submit', methods=['POST'])
def on_submit():
    payload = flask.request.get_json(silent=True)
    if not isinstance(payload, dict):
        return flask.jsonify(status=400, error='Request body must be a JSON object.'), 400

    logging.info('Received quiz submission')
    logging.info(payload)
    with lock:
        try:
            with open(DATA_FILE) as f:
                questions = json.load(f)
        except:
                questions = []
        questions.append(payload)

        with open(DATA_FILE, "w") as f:
             json.dump(questions, f, indent=4)

    return flask.jsonify(status=200, error=None), 200

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80, debug=True)
    