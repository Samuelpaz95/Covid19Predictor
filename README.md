# Covid-19 predictor

Un programa que es capaz de realizar predicciones sobre como va evolucionar la tasa de contagio en los días futuros, el programa puede predecir cuantos casos habran los siguientes tres días considerando la cuarentena, en el escenario mas probable o el peor escenario probable.

Este programa aun esta en fase de pruebas, y solo esta funcionando con los datos de mi pais aunque en teoria deberia funcionar con los datos de cualquier pais.

Este programa está inspirado en el vídeo [Te Explico POR QUÉ estoy PREOCUPADO | [COVID-19]](https://youtu.be/-PUT0hZiZEw) donde muestra como usando matemáticas puede predecir el número de casos posibles en futuros días, les recomiendo ver el video para entender mejor cómo funciona este programa.

## 1. ¿Como funciona?

### 1.1 Análisis.

Tenemos la expresión *I<sub>n+1</sub> = I<sub>n</sub>\*(EP+1)* 

Donde *I<sub>n</sub>* es el número de infectado
y *I<sub>n+1</sub>* es el número de infectado siguiente

Despejamos la variable *EP* ya que esa es la variable que determina un caso futuro y es la variable de la que vamos a predecir los valores posibles que puede tener los siguientes días, según su comportamiento en los días ya registrados.

Tenemos que:

<img src="https://latex.codecogs.com/svg.latex?\Large&space;EP=\frac{I_{n+1}}{I_{n}}-1"/>

Vamos a llamar a la variable *EP* Factor de contagio.

Calculando los valores del *Factor de contagio* en los días registrados tenemos las siguente gráfica.

![figura 1](./.github/Figure_1.png)

### 1.2 Entrenamiento de un modelo.
Para predecir que *Factor de contagio* tendremos en los siguientes días usaremos el algoritmo de regresion lineal, en lugar de simplemente entrenar con los datos y ya, decidi entrenar varios modelos de 5 en 5 datos, es decir recorriendo los datos tomando grupos de 5.

```
[[1,2,3,4,5], 6,7,8,9,10,11,12,13,14,15,16,17,...]
[1, [2,3,4,5,6], 7,8,9,10,11,12,13,14,15,16,17,...]
[1,2, [3,4,5,6,7], 8,9,10,11,12,13,14,15,16,17,...]
[1,2,3, [4,5,6,7,8], 9,10,11,12,13,14,15,16,17,...]
[1,2,3,4, [5,6,7,8,9], 10,11,12,13,14,15,16,17,...]
[...]
[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17, [...]]
```
![figura_2](./.github/Figure_2.gif)
![figura_3](./.github/Figure_2.png)

Obtenemos las siguientes ecuaciones:
- <img src="https://latex.codecogs.com/svg.latex?\Large&space;y_{1}=W_{1}*X + b_{1}"/>
- <img src="https://latex.codecogs.com/svg.latex?\Large&space;y_{2}=W_{2}*X + b_{2}"/>
- <img src="https://latex.codecogs.com/svg.latex?\Large&space;y_{3}=W_{3}*X + b_{3}"/>
- <img src="https://latex.codecogs.com/svg.latex?\Large&space;y_{4}=W_{4}*X + b_{4}"/>
...
- <img src="https://latex.codecogs.com/svg.latex?\Large&space;y_{n}=W_{n}*X + b_{n}"/>

Usamos los parametros *W* y *b* para obtener tres modelos con estas ecuaciones.

- Mediana: <img src="https://latex.codecogs.com/svg.latex?\Large&space;y_{median}=\widetilde{W}*X + \widetilde{b}"/>
- Media: <img src="https://latex.codecogs.com/svg.latex?\Large&space;Y_{mean} =\overline{W}*X + \overline{b}"/>
- Entre las dos anteriores: <img src="https://latex.codecogs.com/svg.latex?\Large&space;Y=W*X + b"/>

![figura_4](./.github/Figure_3.png)

### 1.3 Predicción.

Con estos tres modelos podemos estimar como puede variar el *Factor de contagio* en el futuro.
![figura_4](./.github/Figure_4.png)

EL valor del *Factor de contagio* en los siguientes 10 días puede variar entre la media o la mediana.

### 1.4 Prediccioción del peor escenario probable y el escenario con mayor probabilidad.

En esta parte primero calculo el escenario mas porbable para los proximos 10 días. usando valores aleatorios que se encuentre en area limitada por el modelo de la mediana y la media.

Tambien calculamos el peor escenario con mayor probabilidad, digo esto porque tabien existe el casos extremo en el que todos los contagiados contagien al mismo tiempo.

Para calcular el peor escenario posible hice un calculo iterativo de predecir el dia siguiente tomando el limite superior como futuro *Factor de contagio*, re-entrenar con ese dato adicional y repetir hasta alcanzar los 10 días que dijimos antes. Este seria el resultado de todo.
![figura_5](./.github/Figure_5.png)
![figura_6](./.github/Figure_6.png)

## 2. Conclusiones

Esta es una version alfa de los que estoy desarrollando, en teoria debería funcionar con los datos de otros paises.

## 3. siguientes pasos

- Hacer que este modelo de prediccion sea escalable.
- Añadir ua funcionalidad para poder obtener los datos de forma automatica para poder hacer predicciones en tiempo real, actualmente los datos se obtubieron de forma manual.

## 4. Pre-requisitos para correr el script
- numpy          https://numpy.org/
- matplotlib     https://matplotlib.org/
- scipy          https://www.scipy.org/

## 5. Lanzar el programa

El programa esta escrito en Python 3.

Instalando requisitos:
- Ejecute el siguiente comando para instalar los requisitos
```bash
pip install -r requirements.txt
# o 
pip3 install -r requirements.txt
```
Ejecutar el programa:
- Ejecute
```bash
python covid19_predictor.py 
# o
python3 covid19_predictor.py 

```

## Autores

* **Willy Samuel Paz Colque** - *Trabajo total*