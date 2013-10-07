quizzingbricks-core
===================

Backend for the Quizzing Bricks. Sub components (services etc) are divided into separated folders and isolated from each other.

How to run webapi (flask)
=========================
1. in folder src/python
2. $ gunicorn quizzingbricks.webapi:app -b "0.0.0.0:8100" -k gevent -w 3