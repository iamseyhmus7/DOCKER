from flask import Flask , jsonify
import json

app = Flask(__name__)

@app.route('/datasets',methods = ["GET"])

def get_data():
    with open("datasets.json","r",encoding="utf-8") as file:
        data = [json.loads(line) for line in file]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

