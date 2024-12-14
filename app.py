from flask import Flask, request, render_template, jsonify
from db import db_client


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})


@app.route('/ping', methods=['GET'])
def ping():
    response = db_client.ping()
    return jsonify({'message': response})


if __name__ == '__main__':
    app.run(port=5000)
