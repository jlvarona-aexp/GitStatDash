#Git PR Statistics Dashboard

The intention of this dashboard is to show graphs summarizing the raw Git PR data extracted from github.com, github.aexp.com and Amex bitbucket.

Currently we are extracting git PR data from the following repositories:
* m1-msl
* m1-payments-msl
* m1-ios
* m1-android
* m1-api-contracts

##Technologies
The Dashboard was created using Python and the Plotly Dash libraries. The database is SQLite
* Python 3.8 or greater https://www.python.org/
* Plotly Dash 2.0.0 or greater (Community version) https://community.plotly.com/c/dash/16
* Sqlite 3 https://www.sqlite.org/index.html

##Environment Setup
* Install Python 3. Here is a guide on how to do it on Mac https://programwithus.com/learn/python/install-python3-mac
* Move to the main folder where the repo was cloned
* Verify Python 3 is accessible from this folder by executing:
```
python --version
```
The above should give a result of something like:
```
Python 3.8.9
```
* Load all the dependencies in the Python environment by executing:
```
pip install -r requirements.txt
```

##To run the program
###Command Line
* From the command line, run  this command:
```
python gitstats.py
```
This should show something like the following:
```
Dash is running on http://127.0.0.1:8050/

 * Tip: There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.
 * Serving Flask app 'gitstats' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```
* Open a web browse and navigate to the address and port shown in the screen
###IntelliJ
* Import the project into Intellij
* Let Intellij index and compile
* Run or Debug gitstats.py
* Open a browser and navigate to the address shown on the IntelliJ console


##Configuration
Today the path to the database is hardcoded in dbConnection.py, please change it to your own path. This configuration will eventually be moved to a properties file.