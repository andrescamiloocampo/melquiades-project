# import pandas as pd
# import joblib
# import numpy as np
# from dictionaries import dicts
# from sklearn.linear_model import Ridge
# from sklearn.metrics import mean_squared_error

# time_data = pd.read_csv('./data/timeModel2.csv')
# print(time_data)

# time_data.replace(dicts.area,inplace=True)
# time_data.replace(dicts.routes, inplace=True)

# # Datos de entrenamiento y prueba
# training_data = time_data.sample(frac=0.8,random_state=0)
# test_data = time_data.drop(training_data.index)

# # Training tags

# training_tags = training_data.pop('TIEMPO_PERDIDO')
# test_tags = test_data.pop('TIEMPO_PERDIDO')


# model = Ridge()
# model.fit(training_data,training_tags)
# predicciones = model.predict(test_data)

# print('Margen de error:',np.sqrt(mean_squared_error(test_tags,predicciones)))

# joblib.dump(model, 'time_model.pkl')

import pandas as pd
import joblib
import numpy as np
from dictionaries import dicts
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from dbConnection import getPredictions

# time_data = pd.read_csv('./data/timeModel2.csv')
time_data = getPredictions()

time_data.pop('TIEMPO_ESPERADO')
time_data.pop('TIEMPO_PERDIDO')

time_data.replace(dicts.area,inplace=True)
time_data.replace(dicts.routes, inplace=True)

print(time_data)
# Datos de entrenamiento y prueba
training_data = time_data.sample(frac=0.8,random_state=0)
test_data = time_data.drop(training_data.index)

# Training tags

training_tags = training_data.pop('TIEMPO_REAL')
test_tags = test_data.pop('TIEMPO_REAL')

model = LinearRegression()
model.fit(training_data,training_tags)
predicciones = model.predict(test_data)


input_data = pd.DataFrame(np.array([[1, 11, 3, 1]]),
                              columns=['RUTA', 'BARRIO', 'HORARIO', 'CLIMA'])

print('Prediccion de prueba: ',model.predict(input_data))

print('Margen de error:',np.sqrt(mean_squared_error(test_tags,predicciones)))

joblib.dump(model, 'time_model.pkl')