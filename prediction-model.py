import pandas as pd
import joblib
import numpy as np
from dictionaries import dicts
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression

# Cargar datos
time_data = pd.read_csv('./data/timeModel3.csv')
print(time_data)

# Reemplazar valores según los diccionarios
time_data.replace(dicts.area, inplace=True)
time_data.replace(dicts.routes, inplace=True)

# Generar valores aleatorios en lugar de NaN en 'TIEMPO PERDIDO'
min_value = time_data['TIEMPO PERDIDO'].min()
max_value = time_data['TIEMPO PERDIDO'].max()

# Reemplazar NaN con valores aleatorios en el rango (min_value, max_value)
time_data['TIEMPO PERDIDO'] = time_data['TIEMPO PERDIDO'].apply(
    lambda x: np.random.uniform(min_value, max_value) if pd.isna(x) else x
)

# Datos de entrenamiento y prueba
training_data = time_data.sample(frac=0.8, random_state=0)
test_data = time_data.drop(training_data.index)

# Separar etiquetas de entrenamiento y prueba
training_tags = training_data.pop('TIEMPO PERDIDO')
test_tags = test_data.pop('TIEMPO PERDIDO')

# Entrenar el modelo
model = LinearRegression()
model.fit(training_data, training_tags)

# Realizar predicciones
predicciones = model.predict(test_data)

# Guardar el modelo
joblib.dump(model, 'prediction_model.pkl')
