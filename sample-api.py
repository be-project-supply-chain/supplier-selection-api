import flask
from flask import request, jsonify
from flask_cors import CORS 
from sample_model import load_model
from new_model import call_from_api
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def route():
    return jsonify(books)

@app.route('/sample_model', methods= ['GET'])
def bantai():
    score=load_model()
    return jsonify(score)

@app.route('/neural',methods= ['GET','POST'])
def abc():
    data=request.data
    dataDict = json.loads(data)
    loc=dataDict["location"]
    truck=dataDict["truck_delivered"]
    hand=dataDict["hand_delivered"]
    l=call_from_api(loc,truck,hand)
    out = l.to_json(orient='records')
    # print(out)
    # print(dataDict["location"])
    return out
    

if __name__ == '__main__':
    app.run(debug=True)