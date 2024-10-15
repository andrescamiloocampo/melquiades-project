import pandas as pd
import joblib
import numpy as np
from dictionaries import dicts
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

time_data = pd.read_csv('./data/timeModel2.csv')
print(time_data)

time_data.replace(dicts.area,inplace=True)
time_data.replace(dicts.routes, inplace=True)

# Datos de entrenamiento y prueba
training_data = time_data.sample(frac=0.8,random_state=0)
test_data = time_data.drop(training_data.index)

# Training tags

training_tags = training_data.pop('TIEMPO PERDIDO')
test_tags = test_data.pop('TIEMPO PERDIDO')


model = Ridge()
model.fit(training_data,training_tags)
predicciones = model.predict(test_data)

print('Margen de error:',np.sqrt(mean_squared_error(test_tags,predicciones)))

joblib.dump(model, 'time_model.pkl')