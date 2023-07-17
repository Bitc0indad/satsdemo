from flask import Flask, jsonify
from api.kraken_data import get_data
from flask import render_template

app = Flask(__name__)


# Read up here : https://learnpythonthehardway.org/python3/ex50.html

state = ['CA', 'FL', 'CT', 'NY']

@app.route('/')
def index():
    greeting = "Hello World"
    kraken_data = get_data()
    print(kraken_data)
    kraken_data = "testing kraken data"
    current_state = state[0]
    return render_template("index.html", 
                           greeting=greeting,
                           kraken_data=kraken_data, 
                           state=current_state)


@app.route('/kraken/price')
def kraken_price():
    data = get_data()
    return jsonify(data)




if __name__ == '__main__':
    app.run()
