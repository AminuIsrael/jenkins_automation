import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request
from sklearn.feature_extraction.text import HashingVectorizer
import warnings
warnings.filterwarnings('ignore')
from CustomCode import data_preprocessing

flask_app = Flask(__name__)

model_path = 'ML_model/model.pkl'

@flask_app.route('/', methods=['GET'])
def index_page():
    return_data = {
        "error" : "0",
        "message" : "Successful"
    }
    return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json')

@flask_app.route('/predict',methods=['GET'])
def get_sentiment():
    try:
        user_sentiment = request.json
        if not None in user_sentiment['text'] and not "" in user_sentiment['text']:
            sentiment = user_sentiment["text"]
            #Preprocess_Text
            text = data_preprocessing.clean_tweets(sentiment)
            vect = HashingVectorizer(decode_error='ignore', n_features=2**21, 
                                     preprocessor=None,tokenizer=data_preprocessing.tokenizer)
            clf = pickle.load(open(model_path, 'rb'))
            X = vect.transform([text])
            label = {0:'negative', 1:'positive'}
            prediction = clf.predict(X)[0]
            confidence_score = np.max(clf.predict_proba(X))*100
            status_code = 200
            return_data={
                "error": "0",
                "message": "Successfull",
                "sentiment": label[prediction],
                "confidence_score": confidence_score.round(2)
            }

        else:
            status_code = 400
            return_data = {
                "error": "1",
                "message": "Invalid Parameters"
            }
    
    except Exception as e:
        status_code = 500
        return_data = {
            'error':3,
            'message': str(e)
            }
    
    return flask_app.response_class(response=json.dumps(return_data), mimetype='application/json'),status_code


if __name__ == "__main__":
    flask_app.run(port=9090, debug=True)
