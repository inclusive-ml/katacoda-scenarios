
> Reuse transformations across projects.

### Commençons avec un nouvel environnement

```
ipython
```{{execute}}



## sklearn.pipeline overview

```
# no copy/paste
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

pipe = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),
                      ('scaler', StandardScaler()),
                      ('regressor', RandomForestRegressor())])


pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
```

La pipeline ne se comporte pas vraiment de la même manière quand on fait le fit et la prédiction

## Que se passe-t-il sur un fit pour un StandardScaler

### Données d'entraînement et de validation

```
import numpy as np
train_data = np.array([[1, 10], [2, -1], [0, 22], [3, 15]])
test_data = np.array([[2, 1], [5, 1], [3, 55], [3, 1]])
```{{copy}}

```
train_data
```{{copy}}


```
test_data
```{{copy}}

### Scaler

```
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(train_data)
```{{copy}}

```
scaler.get_params()
```{{copy}}

```
StandardScaler(copy=True, with_mean=True, with_std=True)
```

Quand on construit un modèle (`fit`), la pipeline prend en compte la moyenne et la variance. Mais elle est calculée uniquement sur base des données d'entraînement. Dans la phase de validation ou de prédiction, la moyenne et la variance des données d'entraînement sont utilisées pour une mise à l'échelle.

(les données d'entraînement sont traitées comme population alors que les données test sont traitées comme un échantillon aléatoire)

```
scaler.scale_
```{{copy}}


### Variations entre données d'Entraînement et de Validation

La moyenne pour chaque colonne est de toute évidence différente  pour le set de données d'Entraînement et de Validation


```
train_data.mean(axis=0), test_data.mean(axis=0)
```{{copy}}

### Mise à l'échelle (Scaling)

scaled_train_data

```
scaled_train_data = scaler.transform(train_data)
scaled_train_data
```{{copy}}


scaled_test_data

```
scaled_test_data = scaler.transform(test_data)
scaled_test_data
```{{copy}}

=> Dériver des convertisseurs (transformers) de données sur les données d'entraînement
=> Appliquer ces convertisseurs (transformers) sur les données de validation.
