import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# 1. Cargar los datos
# Reemplaza "ruta_a_tu_archivo.csv" con la ruta del archivo si está en CSV
df = pd.read_csv('./data/timeModel3.csv')

# 2. Preprocesamiento de datos
# Selección de características relevantes
features = ['RUTA', 'BARRIO', 'HORARIO', 'CLIMA', 'VARIACION_CLIMA', 'TIEMPO_DE_RUTA', 'TIEMPO_LLEGADA', 'TIEMPO_REAL', 'TIEMPO_ESPERADO']
X = df[features]
y = df['TIEMPO_PERDIDO']

# Codificación de variables categóricas con OneHotEncoder
encoder = OneHotEncoder(sparse=False)
X_encoded = encoder.fit_transform(X[['RUTA', 'BARRIO', 'CLIMA']])

# Concatenar variables codificadas con las variables numéricas
X_numeric = X.drop(columns=['RUTA', 'BARRIO', 'CLIMA'])
X_final = np.concatenate([X_encoded, X_numeric], axis=1)

# 3. División de los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# 4. Entrenamiento del modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Predicción y evaluación del modelo
y_pred = model.predict(X_test)

# Cálculo de métricas de rendimiento
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Square Error (RMSE): {rmse}")
print(f"R-Squared (R²): {r2}")

# 6. Predicción para nuevos datos
# Ejemplo de predicción: Crea un nuevo conjunto de datos con los mismos campos
nueva_data = pd.DataFrame({
    'RUTA': ['ruta_05'],
    'BARRIO': ['porvenir'],
    'HORARIO': [1],
    'CLIMA': [2],
    'VARIACION_CLIMA': [1],
    'TIEMPO_DE_RUTA': [10],
    'TIEMPO_LLEGADA': [9],
    'TIEMPO_REAL': [20],
    'TIEMPO_ESPERADO': [15]
})

# Codificar la nueva data
nueva_data_encoded = encoder.transform(nueva_data[['RUTA', 'BARRIO', 'CLIMA']])
nueva_data_numeric = nueva_data.drop(columns=['RUTA', 'BARRIO', 'CLIMA'])
nueva_data_final = np.concatenate([nueva_data_encoded, nueva_data_numeric], axis=1)

# Predicción
prediccion = model.predict(nueva_data_final)
print(f"Tiempo perdido estimado: {prediccion[0]}")