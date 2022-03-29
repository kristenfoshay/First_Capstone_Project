<h1 align="center">
    <img width="350" src="https://github.com/kristenfoshay/First_Capstone_Project/blob/main/static/images/ranger-logo-with-text.PNG#gh-light-mode-only" alt="Ranger">
    <br>
    <br>
</h1>

https://ranger-locater.herokuapp.com/

A web application that allows users to make posts and read posts from other users to help find Lost Pets. Users have the ability to drop a marker on a map to indicate where their pet was lost or where they saw a stray pet in the area. 

![Ranger screenshot](https://github.com/kristenfoshay/First_Capstone_Project/blob/main/static/images/ranger-screencapture.PNG)


### App Features Include:

        Users can create profiles to create posts that they lost a pet or have found or sighted one.
        Users can post photos of the animals they have lost or seen.
        Users can drop a marker on a map indicate the exact location of where a pet may have been lost or sighted.
        
 ![Ranger screenshot](https://github.com/kristenfoshay/First_Capstone_Project/blob/main/static/images/ranger-post-creation-screenshot.PNG)   

### Technology Used:

* Python
* Javascript
* Bootstrap
* Flask
* Postgresql
* SQLAlchemy
* Google Maps API

### Getting started with using Ranger locally:

```bash
sudo service postgresql start
createdb ranger
source venv/bin/activate
pip install -r requirements.txt
python seed.py
```

### Future goals for Ranger:

        Ranger could be used to locate other items as well (bikes, wallets, cellphones, gloves, etc.)
        Expand geographic area across North America
        Add the ability for users to message each other when pets are found or sighted. 




