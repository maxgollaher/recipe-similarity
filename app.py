from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
    app.run(port=5000)
