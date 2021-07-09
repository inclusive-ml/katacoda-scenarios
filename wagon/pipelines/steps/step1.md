
## Entraîner une modèle simple

Exemple avec le dataset des frais de taxis de Kaggle (taxi-fare kaggle dataset)

### Travaillons en mode interactif

(les mêmes étapes peuvent être suivient dans un environnement google colab)

```
ipython
```{{execute}}

### Importer les données

```
import pandas as pd
df = pd.read_csv('https://clients.widged.com/wagon/data/taxi-fare-train.csv', nrows=100 )
```{{copy}}

Note: nrows=100. Le dataset original fait plus de 5GB! Il vaut mieux éviter de loader cela en mémoire.

### Exploration des données

```
df.head().T # short for df.head().transpose()
```{{copy}}

```
df.describe().T
```{{copy}}


## Diviser en données d'entraînement et de Validation

Le coût d'un trajet en taxi dépend de:
- point de départ (pickup point)
- point d'arrivée (dropoff point)
- nombre de passagers (passenger count)


=> sklearn.model_selection.train_test_split
- définir un y pour tester les prédictions
- mettre de côté 10% des données pour la validation.

```
from sklearn.model_selection import train_test_split
X = df.drop('fare_amount', axis=1)
y = df['fare_amount']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1, random_state=42)
```{{copy}}


### Vérifions la forme des données

```
X_train.shape, y_train.shape
```{{copy}}

```
X_test.shape , y_test.shape
```{{copy}}

```
df.shape
```{{copy}}


## Pré-traitement


#### Distance Minkowski

Dans les exercices de la semaine dernière, il a été fait mention de la distance **haversine** qui prend en compte la curvature de la planète terre. Il est important de tenir compte de cette curvature pour des longues distances comme de NY à Los Angeles.

=> [Google map](https://www.google.com/maps/@40.7634127,-73.9638161,9.75z), zoom out jusqu'au globe

Mais pour un trajet en taxi, la distance entre le point de départ et le point d'arrivée reste relativement courte.

=>
- ligne droite
- [Manhanttan sur la carte](https://www.google.com/maps/@40.7762803,-73.930264,12.1z)
- Pourquoi l'appele-t-on distance "Manhattan"?
![](https://static.packt-cdn.com/products/9781787121515/graphics/bd978c4c-8251-489d-bcda-5ce7b7b825dd.png)
- La distance Manhattan illustratée
![](https://www.simsoup.info/SimSoup/Manhattan_Distance_Illustration.png)


#### Minkowski comme géneralisation

![](https://prismoskills.appspot.com/lessons/2D_and_3D_Puzzles/imgs/Manhattan_and_Euclidean.png)
- p=2 => euclidian
- p=1 => manhattan

```
def minkowski_distance(start,end, p):
  (x1, y1) = start
  (x2, y2) = end
  return ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) ** (1 / p)

```{{copy}}


### Créons de nouvelles colonnes

Les fonctions de pré-traitement prennent le set de données comme input et fournissent les valeurs pour une nouvelle colonne, distance

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

### Appliquons le pré-traitement

```
X_train_preproc = preprocess(X_train)
X_train_preproc
```{{copy}}

Une seule colonne, la distance.

On peut utiliser ce seul attribut pour créer un modèle.


### Entraînement du modèle

On utilise l'algorithme [_RandomForestRegressor_](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) et on lui présente `X_train_preproc` et `y_train`

> A random forest is a supervised machine learning algorithm that is constructed from decision tree algorithms. It can perform both regression and classification tasks.

En détail: [Random forests outline](https://www.researchgate.net/figure/Random-forests-outline-The-process-starts-with-the-original-data-as-the-input-matrix-In_fig5_273349099)

Dérivation automatique des critères de décision. Ainsi qu'une méthode d'ensemble pour éviter un overfitting aux données d'entraînement.

![](https://www.section.io/engineering-education/introduction-to-random-forest-in-machine-learning/example-of-decision-tree.png)

```
from sklearn.ensemble import RandomForestRegressor
reg = RandomForestRegressor()
reg.fit(X=X_train_preproc, y=y_train)
```{{copy}}

Vérifions les paramètres
```
reg.get_params()
```{{copy}}


```
reg.estimators_
```{{copy}}


## Persistons le modèle sur notre disque dur

[`joblib`](https://joblib.readthedocs.io/en/latest/) est une librairie qui permet de persister un modèle et de le sauver sur un disque.

> Joblib is a set of tools to provide lightweight pipelining in Python. In particular: (1) transparent disk-caching of functions and lazy re-evaluation (memoize pattern) and (2) easy simple parallel computing

Sauver le type de modèle et tous les paramètres definissant le modèle.

=> On va pouvoir réutiliser le modèle en loadant le fichier.

```
import joblib
model_name = 'model.joblib'
joblib.dump(reg, model_name)
```{{copy}}

Vérifions qu'il est bien sauvé.

```
!ls -al
```{{copy}}


### Questions?
