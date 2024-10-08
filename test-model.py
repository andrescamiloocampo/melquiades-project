from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib

# Importamos el dataset
marathon_data = pd.read_csv('./data/MarathonData.csv')

#Eliminamos datos erroneos para el modelo en la columna Wall21
marathon_data['Wall21'] = pd.to_numeric(marathon_data['Wall21'],errors='coerce')

# Eliminamos columnas innecesarias para el modelo
marathon_data = marathon_data.drop(columns=['id'])
marathon_data = marathon_data.drop(columns=['Marathon'])
marathon_data = marathon_data.drop(columns=['CATEGORY'])
marathon_data = marathon_data.drop(columns=['Name'])

# En la columna CrossTraining cambiamos los datos nulos por ceros
marathon_data['CrossTraining'] = marathon_data['CrossTraining'].fillna(0)

# Eliminamos todo registro nulo
marathon_data = marathon_data.dropna(how='any')

# Cambiamos valores de texto por un equivalente numerico
cross_values = {"CrossTraining":{'ciclista 1h':1,'ciclista 3h':2,'ciclista 4h':3,'ciclista 5h':4,'ciclista 13h':5}}
category_values = {"Category":{'MAM':1,'M45':2,'M40':3,'M50':4,'M55':5,'WAM':6}}

marathon_data.replace(cross_values,inplace=True)
marathon_data.replace(category_values,inplace=True)

# 80% de los datos seran para entrenamiento el 20% restante para prueba
training_data = marathon_data.sample(frac=0.8,random_state=0)
test_data = marathon_data.drop(training_data.index)

# Usamos los tags que son utilizados para saber la variable a predecir
training_tags = training_data.pop('MarathonTime')
test_tags = test_data.pop('MarathonTime')

model = LinearRegression()
model.fit(training_data,training_tags)

joblib.dump(model,'test_model.pkl')

# Realizar predicciones con los datos de prueba
# predictions = model.predict(test_data)
