from flask import Flask, jsonify, request
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)