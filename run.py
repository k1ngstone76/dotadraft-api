import json

from flask import Flask, request, jsonify
from joblib import load
import numpy as np
from os import getenv

app = Flask(__name__)

TOP_K = int(getenv("TOP_K", 3))
PORT = int(getenv("PORT", 8080))
ADDRESS = getenv("ADDRESS", "127.0.0.1")

clf = list()

print("Initializing model for step 1 ...")
with open("/app/data/move1/hints.json") as f:
    step1_hints = json.load(f)

clf.append({})  # placeholder for step 0
clf.append({})  # placeholder for step 1
for i in range(2, 23):
    print("Initializing model for step {} ...".format(i))
    clf.append(load('/app/data/move{}/model.joblib'.format(i)))


@app.route('/move/1', methods=['POST'])
def get_stat():
    return jsonify({"status": "ok", "prediction": step1_hints})


@app.route('/move/<int:move>', methods=['POST'])
def predict(move):
    if move < 2 or move > 22:
        return jsonify({"status": "error", "error": "wrong move number"})

    json_data = request.json
    if type(json_data) == list:  # Just moves; use default N for Top N
        moves = json_data
        k = TOP_K
    else:  # Moves and (maybe) N
        moves = json_data["moves"]
        k = json_data["k"] if "k" in json_data.keys() else TOP_K

    query = np.array(moves).reshape(1, -1)
    prediction = clf[move].predict_proba(query)
    top_k_idx = np.argsort(prediction)[0][-1 * k:].tolist()
    top_k_idx.reverse()

    return jsonify({"status": "ok", "prediction": clf[move].classes_[top_k_idx].tolist()})


if __name__ == '__main__':
    app.run(host=ADDRESS, port=PORT)
