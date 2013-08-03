REST-tutorial
=============

Files for my REST API tutorials featuring a server written in Python and a web client written in Javascript. Here are the articles:

- [Designing a RESTful API with Python and Flask](http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
- [Writing a Javascript REST client](http://blog.miguelgrinberg.com/post/writing-a-javascript-rest-client)
- [Designing a RESTful API using Flask-RESTful](http://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful)

Setup
-----

- Install Python 2.7 and git.
- Run `setup.sh` (Linux, OS X, Cygwin) or `setup.bat` (Windows)
- Run `./rest-server.py` to start the server (on Windows use `flask\Scripts\python rest-server.py` instead)
- Alternatively, run `./rest-server-v2.py` to start the Flask-RESTful version of the server.
- Open `http://localhost:5000/index.html` on your web browser to run the client

