Balderdash
==================
Service to support Balderdash app

##Installation
Ensure mysql is installed and then do the following:

```
$ sudo pip install virtualenv
$ cd ~/workspace
$ git clone git@bitbucket.org:smchugh/balderdash.git
$ cd balderdash
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

##Usage
```
$ [ PRINT_SQL=yes ] python run.py
```