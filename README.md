quizzingbricks-core
===================

Backend for the Quizzing Bricks. Sub components (services etc) are divided into separated folders and isolated from each other.

Manual
======

Setup Vagrant
-------------
$ vagrant up dev
$ vagrant ssh dev


Setup development environment for python
----------------------------------------
$ cd /vagrant/
$ sudo python setup.py develop

This install required packages and make our packages available in the environment
which means that we don't need to care about paths.


How to run backend services
===========================
$ python /bin/quizctl.py [name] [-port P] &

Change name to an available service (ex: web) and optionally provide a port.
If you want to see available services, write

$ python /bin/quizctl.py -h

Note: & attach the process to background, use jobs to list all current jobs
or fg to resume to latest.


How to run webapi (flask)
-------------------------
1. in folder src/python
2. $ gunicorn quizzingbricks.webapi:app -b "0.0.0.0:8100" -k gevent -w 3

This starts the RESTful API on port 8100.

Database migrations
===================
We use alembic for database migrations (eg. database changes) and to create a new database migration/revision,
use the following commando
$ alembic revision -m "a message that describe what I am doing"

Which would generate a file under the alembic folder.

1. To upgrade to the latest revision/migration, use
    $ alembic upgrade head

2. To downgrade (redo, delete previous revision), use
    $ alembic downgrade -1

Example can be found in alembic/versions/3899a0e148d3_create_initial_user_.py