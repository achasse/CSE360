### README

Instructions for setting up the project (modified from original copy posted at: https://github.com/CSE360Fall2014/ImageSpace-Django)

## To setup project

* (Ensure python 2.7 is installed)

* Install virtualenv with `easy_install virtualenv`

* Go to a directory workspace and create new virtual environment by `virtualenv <ENV-NAME>`

* activate environment with `source <ENV-DIRECTORY>/bin/activate`

* do `easy_install pip`

* Install dependencies with `pip install -r image_space/requirements.pip`

* Run server with `python manage.py runserver`

* Go to your web browser and open "http://localhost:8000"


*The UI is built with twitter bootstrap, less and jquery*


## Software used
* django 1.7.1
* lettuce 0.2.20 (Testing)
* Selenium (Functional Testing)
* lxml 3.4.0
* nose 1.3.4
* cssselect 0.9.1
* pillow 2.6.1 ImageField in models
* pytz 2014.7
* da_vinci 0.2.1 Brightness edit
* SlickJS for slider
* CamanJS for brightness in-browser edit
* Coverage 3.7.1 (Code coverage)
