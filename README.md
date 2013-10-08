quizzingbricks-core
===================

Backend for the Quizzing Bricks. Sub components (services etc) are divided into separated folders and isolated from each other.

Manual
======

Setup Vagrant
-------------
$ vagrant up dev
$ vagrant ssh dev

Temp: create sqlite db
----------------------
$ cd /vagrant/src/python
$ python bootstrap-db.py


How to run backend services
---------------------------
User service
~~~~~~~~~~~~
$ cd /vagrant/src/python
$ python userservice-bootstrap.py &

Note: & attach the process to background, use jobs to list all current jobs
or fg to resume to latest.


How to run webapi (flask)
-------------------------
1. in folder src/python
2. $ gunicorn quizzingbricks.webapi:app -b "0.0.0.0:8100" -k gevent -w 3

This starts the RESTful API on port 8100.