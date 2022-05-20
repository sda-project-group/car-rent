## Car rental


## Table of contents
* [General info](#general-info)
* [Technologies](#Technologies)
* [Setup](#setup)
* [Features](#Features)


### General info
This is a car rental project made with Django. A car rental company allows you to manage a network of car rental companies.
The application allows you to add and remove cars from the fleet and assign a car to a given user in order to rent a car. The user can browse the cars and rent a car.


### Technologies
Project is created with: 
* Python 3.9.0
* Django 4.0.4
* Pillow 9.1.0
* python-dotenv 0.20.0
* Bootstrap 5


### Setup 
Being a Python web framework, Django requires Python. You can verify that Python is installed by typing python from your shell:
`python3 --version` 

If you don't have Python installed you can go to (https://www.python.org/downloads/) to download it.

Creating a new virtual environment: 
`$ python3 -m venv myenv`

Start the virtual environment with the command:
`myenv\Scripts\activate.ps1`

Then you should clone the repository:
`$ git clone https://github.com/sda-project-group/car-rent.git`
`$ cd car-rent`

Then install the dependencies:
`(myenv)$ pip install -r requirements.txt`

Once pip has finished downloading the dependencies:

`(myenv)$ cd project`
`(myenv)$ python manage.py runserver`

And navigate to http://127.0.0.1:8000




### Features

Client:
* account registration and profile editing
* logging in to the customer account
* password change
* viewing the cars available at the rental company
* renting a car in a selected period of time after checking if the car is available
* checking customer orders (pending, past and future)


Administrator:
* creating accounts for employees
* deleting and editing customer and employee accounts
* granting permissions to users
* approval of car edits
* adding cars to the fleet
* car removal

Employee:
* editing cars (must be approved by the administrator)
