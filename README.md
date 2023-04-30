# **Microservicio para determinar el precio de los vehículos en Estados Unidos**
Este es un microservicio que tiene como objetivo determinar el precio de los vehículos en Estados Unidos. Para ello, se utilizan varios modelos de aprendizaje automático que han sido entrenados con datos históricos de precios de vehículos.

## **Estructura del proyecto**
El proyecto está organizado de la siguiente manera:

- .gitignore: archivo que indica qué archivos y carpetas no se deben incluir en el repositorio.
requirements.txt: archivo que contiene las librerías necesarias para ejecutar el proyecto y sus respectivas versiones.
- INPUT/: carpeta que contiene los datos de entrenamiento, prueba y validación utilizados para construir los modelos.
- SCRIPTS/: carpeta que contiene el notebook de exploración de datos y generación de modelos mediante joblib, el módulo para levantar la API mediante FLASK, y el modelo ya entrenado.
- OUTPUT/: carpeta que contiene los archivos binarios del procesamiento de información y el modelo ya entrenado.

## **Funcionamiento**
Para utilizar el microservicio, primero es necesario ejecutar el script que levanta la API mediante Flask. Una vez que la API está en funcionamiento, se pueden enviar solicitudes HTTP para obtener predicciones de precios de vehículos.

El modelo utilizado para hacer las predicciones se ha entrenado con datos históricos y utiliza varias características de los vehículos (marca, modelo, año, kilometraje, etc.) para predecir el precio del vehículo.

## **Requerimientos**
Es necesario tener instalado Python 3 y las librerías que se encuentran en el archivo requirements.txt.
Para instalar las librerías necesarias, se puede utilizar el siguiente comando en la terminal:
$pip install -r requirements.txt

## **Instrucciones de uso**
Para utilizar el microservicio, siga los siguientes pasos:

1. Clone este repositorio en su máquina local:
$git clone https://github.com/<username>/microservicio-precio-vehiculos.git

2. Navegue hasta la carpeta donde se encuentra el proyecto:
$cd microservicio-precio-vehiculos

3. Instale las librerías necesarias:
$pip install -r requirements.txt

4. Ejecute el script que levanta la API mediante Flask:
$python SCRIPTS/api.py

5. Envíe solicitudes HTTP a la API para obtener predicciones de precios de vehículos.
$http://13.59.116.134:5000/predict/?Year=2014&Mileage=31909&State=_FL&Make=Nissan&Model=MuranoAWD
