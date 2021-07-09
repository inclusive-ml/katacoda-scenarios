
## Commençons avec un nouvel environnement

```
ipython
```{{execute}}

## Time features

```
# no copy/paste
def feat_eng_on_date(df, col):
    """create new feat based on date :
    day of week, month, weekend, median"""
    df['date'] = df[col].astype('datetime64[ns]')
    df['weekend'] = (df.date.dt.dayofweek // 5 == 1).astype(float)
    df['dow'] = df.date.dt.dayofweek
    df['year'] = df.date.dt.year
    df['month'] = df.date.dt.month
    df['day'] = df.date.dt.day
    df['month_end'] = df.date.dt.is_month_end.astype(float)
    df['month_begin'] = df.date.dt.is_month_start.astype(float)
    return df
```

## Geolocation

[Geohashing](http://geohash.gofreerange.com/)

![](https://miro.medium.com/max/1400/1*klMZxWeXGJCP1x1TVNYKuw.png)

![](https://miro.medium.com/max/1400/1*ubDJJQrnzqw4kQzvSGJkgg.png)

![](https://miro.medium.com/max/1400/1*Ztuopn00LqObHQb3v5r8aQ.png)



## Extracting a few features

Repartons des données taxifare

```
import pandas as pd
df = pd.read_csv('https://clients.widged.com/wagon/data/taxi-fare-train.csv', nrows=100 )
df.head().T
```{{copy}}


# Quelques variables dérivées de temps

```
df['pickup_datetime'] = df.pickup_datetime.apply(pd.to_datetime)
df.dtypes
```{{copy}}


```
df['dow'] = df.pickup_datetime.dt.dayofweek
df['hour'] = df.pickup_datetime.dt.hour
df.head().T
```{{copy}}

# Quelques variables dérivées de distance

```
def minkowski_distance(start,end, p):
  (x1, y1) = start
  (x2, y2) = end
  return ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) ** (1 / p)

```{{copy}}

```
x1, y1 = df["pickup_longitude"], df["pickup_latitude"]
x2, y2 = df["dropoff_longitude"], df["dropoff_latitude"]
df['distance'] = minkowski_distance((x1, y1),(x2, y2), p=1)
df.head().T

```{{copy}}

## Passons toutes les variables disponibles en revue


```
df.describe().T
```{{copy}}

## Laissons de côté quelques colonnes

```
X_train = df.drop(['fare_amount', 'key', 'pickup_datetime'], axis=1)
y_train = df['fare_amount']
```{{copy}}

Forme des données
```
X_train.shape, y_train.shape
```{{copy}}

```
X_train.head().T
```{{copy}}

## Créons une pipeline toute simple

```
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

pipe = Pipeline(steps=[
  ('imputer', SimpleImputer(strategy='median')),
  ('scaler', StandardScaler()),
  ('regressor', RandomForestRegressor())])
```{{copy}}

3 étapes successives:
- `imputer` pour remplacer toute donnée qui serait manquante
- `scaler` pour normalizer les données (s'applique seulement aux données numériques; si on avait des données texte, donnerait lieu à une erreur)
- `regressor` applique une régression "Random Forest"


```
pipe
```{{copy}}


## Créer le modèle (fitting)

Créons le modèle sur base des données d'entraînement.

Phase d'entraînement
```
pipe.fit(X_train, y_train)
```{{copy}}

phase d'inférence

```
y_pred_train = pipe.predict(X_train)
y_pred_train
```{{copy}}


Note : nous avons appliqué les mêmes transformations à toutes les colonnes. D'habitude, on veut appliquer des types et séquences de transformations différentes sur des types de colonnes.


**Questions?**

## Intégrer des étapes customisées

Nous devons utiliser une classe
- héritant de BaseEstimator et TransformerMixin
- définissant une fonction `fit` et une function `transform`.

```
from sklearn.base import BaseEstimator, TransformerMixin

class HourTransformer(BaseEstimator, TransformerMixin):

  def __init__(self, time_column, time_zone_name='America/Los_Angeles'):
      self.time_column = time_column
      self.time_zone_name = time_zone_name

  def fit(self, X, y=None):
      return self

  def transform(self, X, y=None):
      assert isinstance(X, pd.DataFrame)
      X.index = pd.to_datetime(X[self.time_column])
      X.index = X.index.tz_convert(self.time_zone_name)
      X["hour"] = X.index.hour
      return X[["hour"]].reset_index(drop=True)
```{{copy}}


Si on effectue une mise en échelle, il peut être nécessaire de  dériver et capturer certains paramètres pendant la phase de fit (mean and variance for standardScaler), sauver leur étant dans la classe, les réutiliser dans la phase de transform.

### Example: implémentons un standard scaler customisé

Il faut définir une classe qui hérite de BaseEstimator, TransformerMixin

```
from sklearn.base import BaseEstimator, TransformerMixin

class CustomStandardScaler(BaseEstimator, TransformerMixin):
```{{copy}}

On en viendra a instantier cette classe de cette manière:

```
# no copy/paste
taxifare_dataset_std_scaler = CustomStandardScaler()
# training
taxifare_dataset_std_scaler.fit(X_train)
taxifare_dataset_std_scaler.transform(X_train)
# inference
taxifare_dataset_std_scaler.transform(X_test)
```

La classe doit avoir une méthode `__init__`

```
  def __init__(self):
      pass
```{{copy}}


```
  def fit(self, X, y=None):
    # X is a multi-columns dataset, so we would
    # need to store an array of values
    self.mus = list()
    self.sigmas = list()
    for column in X:
        self.mus.append(column.mean())
        self.sigmas.append(column.std())
    return self
```{{copy}}

Les valeurs sont attachées à self, qui encode l'état de l'instance courrante.

```
  def transform(self, X, y=None):
    for i, column in enumerate(column):
        self.mus.append(column.mean())
        self.sigmas.append(column.std())
    return (X - self.mus[i])/self.processed_sigma[i]
```{{copy}}

### Retournons au feature engineering

```
from sklearn.base import BaseEstimator, TransformerMixin

class HourTransformer(BaseEstimator, TransformerMixin):

  def __init__(self, time_column, time_zone_name='America/Los_Angeles'):
      self.time_column = time_column
      self.time_zone_name = time_zone_name

  def fit(self, X, y=None):
      return self

  def transform(self, X, y=None):
      assert isinstance(X, pd.DataFrame)
      X.index = pd.to_datetime(X[self.time_column])
      X.index = X.index.tz_convert(self.time_zone_name)
      X["hour"] = X.index.hour
      return X
```{{copy}}

Créons une instance de la classe.

```
feat_encoder = HourTransformer(time_column='pickup_datetime', time_zone_name='America/Los_Angeles')
```{{copy}}

#### Exécuter la pipeline - Fit et Transform

"Fit" de note pipeline (même si dans ce cas aucune opération n'est effecctuée)

```
feat_encoder.fit(X_train)
```{{copy}}

Transform

```
X_train = df.drop(['fare_amount', 'key'], axis=1)
X_processed = feat_encoder.transform(X_train)
X_processed[["hour"]]
```{{copy}}

=> Il est maintenant possible d'appliquer des transformations différentes sur différentes colonnes
