<h1 align="center">
    <img width="350" src="https://github.com/kristenfoshay/First_Capstone_Project/blob/main/static/images/ranger-logo-with-text.PNG#gh-light-mode-only" alt="Ranger">
    <br>
    <br>
</h1>

https://ranger-locater.herokuapp.com/

A web application that allows users to make posts and read posts from other users to help find Lost Pets. Users have the ability to drop a marker on a map to indicate where their pet was lost or where they saw a stray pet in the area. 

![Ranger screenshot](https://github.com/kristenfoshay/First_Capstone_Project/blob/main/static/images/ranger-screencapture.PNG)


## App Features Include:

        Users can create profiles to create posts that they lost a pet or have found or sighted one.
        Users can post photos of the animals they have lost or seen.
        Users can drop a marker on a map indicate the exact location of where a pet may have been lost or sighted.
        
 ![Ranger screenshot](https://github.com/kristenfoshay/First_Capstone_Project/blob/main/static/images/ranger-post-creation-screenshot.PNG)   

## Technology Used:

* Python
* Javascript
* jQuery
* Bootstrap
* Flask
* SQLAlchemy
* Google Maps API

## Getting started with using Ranger locally:

### Create a new directory inside of which Ranger will be stored, then navigate to be inside this new directory and create a virtual environment for the project:

```bash
python3 -m venv venv
```
### Activate the virtual environment, and once there proceed to installing the requirements for Ranger to work using the requirements.txt:

```bash
source venv/bin/activate
pip install -r requirements.txt
```
### Creating the database, start the Postgresql server and create the "ranger" database:

```bash
sudo service postgresql start
createdb ranger
```
### Seed the database with important data by running seed.py:

```bash
python seed.py
```

## Testing Ranger:

### There are 3 provided unit tests to make sure Ranger is working properly. Run them using python in your virtual environment from the project's home directory. For example, run "test_post_model.py" the following way:

```python
source venv/bin/activate
python -m unittest test_post_model.py
```

## Future goals for Ranger:

### Ranger is a useful way of connecting users who need to find stuff:

        Ranger could be used to locate other items as well (bikes, wallets, cellphones, gloves, etc.)
### Ranger is not just useful for the Greater Toronto Area:

        We plan to expand its scope across a larger geographic area, all of North America and beyond.
### Lost and Found is easier to do when users are actually able to connect:

        We are in the process of adding the ability for users to message each other when pets are found or sighted. 




