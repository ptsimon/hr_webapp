# Employee Check-In Manager
For Thinking Machines Enterprise Solutions Engineering L1 Exam

This web application displays and searched through employee check-in logs, uploads csv files to database, and logs a check-in. 
A Python Flask backend is used to talk to a SQLite database through SQLAlchemy and Bootstrap is used to format the forms and tables.

## Setup
1. Ensure you have Python 3 installed (project was developed using Python 3.8). Installation instructions are provided [here](http://docs.python-guide.org/en/latest/starting/installation/).
2. Ensure you have `virtualenv` or `venv` (I used venv) installed as a virtual environment will be needed to run the Flask server. Installation instructions can be found [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
3. Create a virtualenv in the root of the project and install requirements:
```
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -r requirements.txt
```

## Usage
1. Initiate the Flask server (if no port parameter is provided it will be set to run on port 5000):
```
$ python3 run.py
```
3. Navigate to `localhost:5000` to see the application.