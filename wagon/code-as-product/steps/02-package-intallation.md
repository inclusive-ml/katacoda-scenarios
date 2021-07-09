## Objective

Install your first package called `mlproject`

## Your first package

Now navigate outside of your `data-challenges` directory and create a new `mlproject`:

```bash
cd ~/sandbox/02-Package-installation/
wagon-make-package mlproject
```{{execute}}

The ultimate goals of our `mlproject` are:

- install it as a package
- install scripts

Get inside `mlproject`

```bash
cd mlproject
```{{execute}}


👉 Inspect script under `scripts/mlproject-run` (you might have to click on the refresh button)
👉 Inspect code you want to package as a module under `mlproject/`

You'll want to install these dependencies and the script.

To install your package, as seen in lecture, simply run:

```bash
pip install .
```{{execute}}

💡 **Here pip understands what he has to do thanks to his buddy and MVP `setup.py` file**
💡 **Thanks to his MVP, he knew he had to install dependencies from `requirements.txt`**

## Project as a package

Your mlproject is now a package, just like pandas or sklearn

Go anywhere you want and run inside either `ipython` or a `python` interpreter or a notebook:

```bash
ipython
```{{execute}}


```python
from mlproject.lib import clean_data
clean_data
```{{execute}}

Exit the REPL

```python
exit()
```{{execute}}


## Project as scripts

You also have installed a script, test it in your terminal:

```bash
mlproject-run
```{{execute}}

## Your first module now

Create a new python file called `mlproject/distance.py` inside which you'll add the following function

```bash
touch mlproject/distance.py
```{{execute}}

Go to the editor, hit refresh if you need to. Paste the following.

```python
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r
```{{copy}}

To check if your function works, a good practice is to add `if __name__ == "__main__"` at the end of `distance.py` and compute your first distance:

```python
if __name__ == "__main__":
    # Le Wagon location
    lat1, lon1 = 48.865070, 2.380009
    #Insert your coordinates from google maps here
    #lat2, lon2 = x, y
    distance = haversine(lon1, lat1, lon2, lat2)
    print(distance)
```{{copy}}

🤔[Here's a link](https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/) to understand what the condition above does if it's not clear


To find the `x,y`, enter a location in google map. You will get an address like `https://www.google.com/maps/place/Bruxelles/@50.8549541,4.3053504,12z/`. `x` is `50.8549541` and `y` is  `4.3053504`.

Then run :

```bash
python -i mlproject/distance.py
```{{execute}}

If you see `>>>` in your terminal after running this commmand, it's completely normal. the `-i` stands for interactive mode. This means that you can explore the variables you created in your python script. To exit the interactive mode either type `exit()` or `CTRL-D`.

💡 **You could also run `%run mlproject/distance.py` inside a notebook or ipython interpreter (do not forget to `import mlproject.lib`, you must be located in `mlproject/`)**

Exit the REPL

```bash
exit()
```{{execute}}

```bash
tree
```{{execute}}

Your new tree should look like:

```bash
├── MANIFEST.in
├── Makefile
├── README.md
├── mlproject
│   ├── __init__.py
│   ├── data
│   │   └── data.csv.gz
│   ├── distance.py
│   └── lib.py
├── requirements.txt
├── scripts
│   └── mlproject-run
├── setup.py
└── tests
    ├── __init__.py
    └── lib_test.py
```

Install package and start using your new function from anywhere you want (you need to be located inside the `mlproject` directory):

```bash
make install
```{{execute}}

In any notebook:

```bash
ipython
```{{execute}}

```python
from mlproject.distance import haversine
haversine
```{{execute}}

👆You should now be able to use your `haversine` function in the notebook.

Exit the REPL
```bash
exit()
```{{execute}}

## Your own script now

The objective here is to implement a new script under `scripts/` called mlproject-computedist taking as parameters 4 (long1, lat1, long2, lat2) and returning the haversine distance.

Install termcolor to allow your script to output colored text `pip install termcolor`.

```python
pip install termcolor
```{{execute}}


You can inspect code from `computedist.py` (or `script.py`) file located in `~/sandbox/02-Package-installation`

```bash
cd ~/sandbox/02-Package-installation
```{{execute}}

to understand how to give arguments to a script.

Run :

```bash
python computedist.py --coords 48.865 2.380 48.235 2.393
```{{execute}}


Basically you'll want to run the exact same command but without `python` and anywhere on your laptop.
For that simply:

- Create `scripts/mlproject-computedist` file with the exact same code as in `computedist.py`
  👉 **no `.py` at the end of scripts**
- Add the following lines at the beginning of the file. The first line specifies that the file is a python script. The second line specifies that the file is encoded using UTF-8 characters.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```

- Modify `setup.py` in order to add `mlproject-computedist` to the list of scripts

```bash
tree
```{{execute}}


Your new tree should look like:

```bash
├── MANIFEST.in
├── Makefile
├── README.md
├── mlproject
│   ├── __init__.py
│   ├── data
│   │   └── data.csv.gz
│   ├── distance.py
│   └── lib.py
├── requirements.txt
├── scripts
│   ├── mlproject-computedist
│   └── mlproject-run
├── setup.py
└── tests
    ├── __init__.py
    └── lib_test.py
```

And your `setup.py` slightly modified:

```python
from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='mlproject',
      version="1.0",
      description="Project Description",
      packages=find_packages(),
      test_suite = 'tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      scripts=['scripts/mlproject-run', 'scripts/mlproject-computedist'],
      zip_safe=False)
```{{execute}}

Finally install package and scripts:

```python
make install
```{{execute}}

And test your script

```bash
mlproject-computedist --help
```{{execute}}

```bash
mlproject-computedist --coords 48.865070 2.380009 48.235070 2.393409
```{{execute}}

To go further on parsing arguments, check [that link](https://www.sicara.ai/blog/2018-12-18-perfect-command-line-interfaces-python)
