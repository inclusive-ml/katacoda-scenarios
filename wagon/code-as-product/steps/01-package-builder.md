## Install Package builder with pip

Before doing anything here, please make sure _**you are inside a python3 virtual environment**_

```bash
pip install wagon-tools
```{{execute}}

As seen in this morning's lecture, quite a lot of things happened. You have installed:

- `wagon_tools` package and its modules:
- `wagon-make-package` script

This script will be your package builder.

# Use package builder

Now let's suppose you start a new ML project, you want to package your code somewhere.

You now have access to a cool script that you can run from anywhere on your laptop

Go to `sandbox/01-Package-builder/` to test the script, and build your first package:

```bash
cd sandbox/01-Package-builder/ && wagon-make-package first_project
```{{execute}}

Get inside you newliy created paskage

```bash
cd first_project
```{{execute}}

Here is the project structure where you'll want to use to package your code.
Check how your package is structured by running `tree` inside your terminal

```
$ tree
├── MANIFEST.in
├── Makefile
├── README.md
├── first_project
│   ├── __init__.py
│   ├── data
│   │   └── data.csv.gz
│   └── lib.py
├── requirements.txt
├── scripts
│   └── first_project-run
├── setup.py
└── tests
    ├── __init__.py
    └── lib_test.py
````
