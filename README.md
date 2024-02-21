# Rent Track System 

Rent Track System is a web-application that helps you manageing your real-state rents. 

- Easy To Use 

## Features

- You can save notes for each apartment. 
- You can be notified in the paying-date by a whatsapp message. 


## Tech

Rent-Track-System uses a number of open source projects to work properly:

- [Bootstrap5] - HTML enhanced for web apps!
- [VS-Code] - Main Text Editor
- [HTMX] - For Sending AJAX Requests
- [Django] - For Backend Sever Side 
- [SQLITE3] As the main db 

And of course Rent-Track-System itself is open source with a [public repository](https://github.com/YousefSedik/rent-track-system/)
 on GitHub.

## Installation

Rent-Track-System requires [Python](https://www.python.org/downloads/) v3+ a to run.

Create A Virtual Enviroment 
```sh
pip install venv 
python -m venv venv
```
Activate The Virtual Enviromnent 
```sh
\venv\Scripts\activate.bat
```
Install the dependencies and devDependencies
```sh
pip install -r requiremints.txt
py manage.py migrate 
```
Then You Can Run The Development Directly
```sh
py manage.py runserver  
```

