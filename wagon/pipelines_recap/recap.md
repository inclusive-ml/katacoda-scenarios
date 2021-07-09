
> The objective of this exercise is to use the tools and methods you learnt during the previous weeks, in order to solve a **real challenge**.
>
> The problem to solve is a **Kaggle Competition**: [New York City Taxi Fare Prediction](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction). The goal is to predict the fare amount (inclusive of tolls) for a taxi ride in New York City given the pickup and dropoff locations.


## Prepare the environment

```
ipython
```{{execute}}

# Recap

Building a machine learning model requires a few different steps

## Steps
1. [Get the data](#part1)
2. [Explore the data](#part2)
3. [Data cleaning](#part3)
4. [Evaluation metric](#part4)
5. [Model baseline](#part5)
6. [Build your first model](#part6)
7. [Model evaluation](#part7)
8. [Kaggle submission](#part8)
9. [Model iteration](#part9)

## 1. Get the data <a id='part1'></a>

The dataset is available on [Kaggle](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data)

First of all:
- Follow the instructions to download the training and test sets
- Put the datasets in a separate folder on your local disk, that you can name "data" for example.

Now we are going to use Pandas to read and explore the datasets.

```
import pandas as pd
```{{copy}}


The training dataset is relatively big (~5GB).
So let's only open a portion of it.
👉 Go to [Pandas documentation](https://pandas.pydata.org/pandas-docs/stable/) to see how to open a portion of csv file and store it into a dataframe. (ex: just read 1 million rows maximum)
💡 NB: here we will read portion of a file **directly from an url**, texactly the same can be done with local file

```
url = 'https://clients.widged.com/wagon/data/taxi-fare-train.csv'
df = pd.read_csv(url, nrows=1000)
```{{copy}}


Now let's display the first rows to understand the different fields

```
df.head(2).T
```{{copy}}

## 2. Explore the data <a id='part2'></a>

Before trying to solve the prediction problem, we need to get a better understanding of the data.
For that, libraries like Pandas and Seaborn are your best friends.
Firt of all, make you sure you have [Seaborn](https://seaborn.pydata.org/) installed and import it into your notebook. Note that this can be also useful to import `matplotlib.pyplot` to customize a few things.

```
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 14
plt.figure(figsize=(12,5))
palette = sns.color_palette('Paired', 10)
```{{copy}}



### There are multiple things we want to do in terms of data exploration.

- You first want to look at the distribution of the variable you are going to predict: "fare_amount"
- Then you want to vizualize other variable distributions
- And finally it is often very helpful to compute and vizualise correlation between the target the variable and other variables.
- Also, look for any missing values, or other irregularities.


### Explore the target variable
- Compute simple statistics of the target variable (min, max, mean, std, ...)
- Plot distributions


```
df.fare_amount.describe()
```{{copy}}



```
#%matplotlib inline
def plot_dist(series=df["fare_amount"], title="Fare Distribution"):
    sns.distplot(series)
    sns.despine()
    plt.title(title);
    plt.show()
plot_dist()
```{{copy}}



```
# drop absurd values
df = df[df.fare_amount.between(0, 6000)]
plot_dist(df.fare_amount)
```{{copy}}


```
# We can also visualise binned fare_amount variable
df['fare-bin'] = pd.cut(df['fare_amount'], bins = list(range(0, 50, 5))).astype(str)

# Uppermost bin
df.loc[df['fare-bin'] == 'nan', 'fare-bin'] = '[45+]'

# Adjust bin so the sorting is correct
df.loc[df['fare-bin'] == '(5, 10]', 'fare-bin'] = '(05, 10]'
```{{copy}}


```
sns.catplot(x="fare-bin", kind="count", palette=palette, data=df, height=5, aspect=3);
sns.despine()
plt.show()
```{{copy}}


### Explore other variables

- passenger_count (statistics + distribution)
- pickup_datetime (you need to build time features out of pickup datetime)
- Geospatial features (pickup_longitude, pickup_latitude,dropoff_longitude,dropoff_latitude)
- Find other variables you can compute from existing data that might explain the target

#### Passenger Count

```
df.passenger_count.describe()
```{{copy}}


```
sns.catplot(x="passenger_count", kind="count", palette=palette, data=df, height=5, aspect=3);
sns.despine()
plt.title('Passenger Count');
plt.show()
```{{copy}}



#### Pickup Datetime
- Extract time features from pickup_datetime (hour, day of week, month, year)
- Create a method `def extract_time_features(_df)` that you will be able to re-use later
- Be careful of timezone
- Explore the newly created features

```
def extract_time_features(df):
    timezone_name = 'America/New_York'
    time_column = "pickup_datetime"
    df.index = pd.to_datetime(df[time_column])
    df.index = df.index.tz_convert(timezone_name)
    df["dow"] = df.index.weekday
    df["hour"] = df.index.hour
    df["month"] = df.index.month
    df["year"] = df.index.year
    return df.reset_index(drop=True)
```{{copy}}



```
# %%time
df = extract_time_features(df)
```{{copy}}


```
# hour of day
sns.catplot(x="hour", kind="count", palette=palette, data=df, height=5, aspect=3);
sns.despine()
plt.title('Hour of Day');
plt.show()
```{{copy}}
