### Commençons avec un nouvel environnement

````
exit()
```{{execute}}

````

curl https://clients.widged.com/wagon/data/model.joblib > model.joblib

```{{execute}}

```

ipython

```{{execute}}


### Chargeons le modèle avec joblib


```

import joblib
model_name = 'model.joblib'
loaded_model = joblib.load(model_name)

```{{copy}}

Vérifions que c'est bien le même modèle

```

loaded_model.get_params()

```{{copy}}

Les critères d'estimation

```

loaded*model.estimators*

```{{copy}}


### Tentons une prédiction

Ici on répête les étapes précédentes

```

import pandas as pd
df = pd.read_csv('https://clients.widged.com/wagon/data/taxi-fare-train.csv', nrows=100 )

```{{copy}}

```

from sklearn.model_selection import train_test_split
X = df.drop('fare_amount', axis=1)
y = df['fare_amount']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1, random_state=42)

```{{copy}}


```

y_pred = loaded_model.predict(X_test)
y_pred

```{{copy}}

### UhOh! Erreur!

Quel est le problème à votre avis?

Lisons le message d'erreur...

> ValueError: could not convert string to float: '2013-07-08 21:24:00.00000048'

Nous avous oublié d'appliquer les étapes de préprocessing!


```

def minkowski_distance(start,end, p):
(x1, y1) = start
(x2, y2) = end
return ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) \*\* (1 / p)

```{{copy}}

```

def preprocess(df):
"""add a column with the manhattan distance"""
x1, y1 = df["pickup_longitude"], df["pickup_latitude"]
x2, y2 = df["dropoff_longitude"], df["dropoff_latitude"]
distance = minkowski_distance((x1, y1),(x2, y2), p=2)
res = df.copy()
res["distance"] = distance
return res[["distance"]]

```{{copy}}


```

X_test_preproc = preprocess(X_test)
X_test_preproc.head()

```{{copy}}

Ok, on a les attributs (features) du modèle dans le format attendu. Re-essayons une prédiction.

```

y_pred = loaded_model.predict(X_test_preproc)
y_pred

```{{copy}}



=> Nous avons une prédiction du coût en fonction de la distance

```

[13.4124 4.5555 5.981 11.477 5.344 13.75 5.11 8.472 6.547
5.11 ]

```

Et le coût en fonction de la distance


```

pd.concat([pd.DataFrame(X_test_preproc.to_numpy(), columns=['distance']), pd.DataFrame(y_pred, columns=['fare_predicted'])], axis=1)

```{{copy}}

Output:

```

distance fare_predicted
0 0.058789 12.860
1 0.002247 4.840
2 0.010245 5.730
3 0.023348 12.000
4 0.011100 4.980
5 0.032301 14.713
6 0.009260 5.020
7 0.017435 8.150
8 0.016020 7.620
9 0.009436 5.020

```

### Evaluation du modèle

On a fait bcp de copier/coller de code.

En pseudocode, effectuer une prédiction devrait inclure les étapes suivantes:

```

# -- preprocess --

X = preprocess(df)

# -- load model --

import joblib
model = joblib.load('model.joblib')

# -- predict --

predictedFare = model.predict(X)
predictedFare

```{{copy}}

Ce sont en fait deux pipelines différentes

```

|=> preprocess data |
|=> predict |
|=> loadModel |

```

```
