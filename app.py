from flask import Flask, jsonify, request
import pandas as pd
import joblib
import numpy as np
from dbConnection import seedPredictions,insertPrediction
from timeModel import train
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load('time_model.pkl')

@app.route('/prediction')
def prediction():
    input_data = pd.DataFrame(np.array([[1, 1, 2, 1, 20, 25]]),
                              columns=['RUTA', 'BARRIO', 'HORARIO', 'CLIMA', 'TIEMPO REAL','TIEMPO ESPERADO'])
    prediction = model.predict(input_data)
        
    prediction_list = prediction.tolist()
    
    if len(prediction_list) == 1:
        prediction_value = prediction_list[0]
    else:
        prediction_value = prediction_list
    
    response = {"prediction": prediction_value}

    return jsonify(response)

@app.route('/predictionPost',methods=['POST'])
def predictionPost():
    if(request.method == 'POST'):
        body = request.get_json()
        
        input_data = pd.DataFrame(np.array([list(body.values())]),columns=list(body.keys()))
        prediction = model.predict(input_data)
        prediction_list = prediction.tolist()

        if len(prediction_list) == 1:
            prediction_value = prediction_list[0]
        else:
            prediction_value = prediction_list
    
        response = {"prediction": prediction_value}

        return jsonify(response)
    
@app.route('/newPrediction',methods=['POST'])
def newPrediction():
    predictionModel = joblib.load('prediction_model.pkl')
    if(request.method == 'POST'):
        body = request.get_json()
        
        input_data = pd.DataFrame(np.array([list(body.values())]),columns=list(body.keys()))
        prediction = predictionModel.predict(input_data)
        prediction_list = prediction.tolist()

        if len(prediction_list) == 1:
            prediction_value = prediction_list[0]
        else:
            prediction_value = prediction_list
    
        response = {"prediction": prediction_value}

        return jsonify(response)    
    
@app.route('/createPrediction',methods=['POST'])
def createPrediction():
    if(request.method == 'POST'):
        body = request.get_json()
        try:
            print(body)
            response = insertPrediction(body)
            return jsonify(response)
        except Exception as e:
            print(f"Request error: {e}")
            return f"Error: {e}"        
        
    return jsonify('None')

@app.route('/hello')
def hello():
    return jsonify('HELLO')

@app.route('/train')
def trainModel():
    res = train()
    return jsonify(res)


@app.route('/databaseSeeder',methods=['POST'])
def databaseSeeder():        
    return seedPredictions()    

if __name__ == '__main__':
    app.run()