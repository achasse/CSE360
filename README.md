### README
This is the skeleton for image hosting and editing app called ImageSpace in Django Python. You can name your project anything you want.

To continue your project on top of this, clone this code and do following. (Assumed python 2.7 is already installed)

## To setup project

* Install virtualenv with `easy_install virtualenv`

* Go to a directory workspace and create new virtual environment by `virtualenv <ENV-NAME>`

* activate environment with `source <ENV-DIRECTORY>/bin/activate`

* do `easy_install pip`

* Install dependencies with `pip install -r image_space/requirements.pip`

* Run server with `python manage.py runserver`

* Go to your web browser and open "http://localhost:8000"

* You are ready to roll :)


*The UI is built with twitter bootstrap, less and jquery*


## To run sample unit test

* run `python manage.py test image_space_app/tests`

The source file for test is at image_space/image_space_app/tests folder.

## To run sample functional test

*run `python manage.py harvest`

*The functional test is written on Lettuce steps. You can see the tests at image_space/image_space_app/features folder*

## Software used
* django 1.7.1
* lettuce 0.2.20 (Testing)
* lxml 3.4.0
* nose 1.3.4
* cssselect 0.9.1
* pillow 2.6.1 ImageField in models
* pytz 2014.7
* da_vinci 0.2.1 Brightness edit
* SlickJS for slider
* CamanJS for brightness in-browser edit
* Coverage 3.7.1 (Code coverage)
