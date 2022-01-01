# Book service for GridU course Python for QA 

### Book Service API

Book as an entry has:
* Title(String(length<256 symbols))
* Type (String, listed below)
* ID(String) (should be unique, uuid4)
* Creation date (YYYY-MM-DD) (can be null)
* Updated date time (ISO 8601) 

Book following types are supported:
* Science
* Satire
* Drama
* Action and Adventure
* Romance 

The following methods are implemented:
* /v1/books/manipulation POST - Add book with no arguments but request payload as json contains fields  (type, title, creation date)
* /v1/books/manipulation DELETE - Delete book with arguments (id)
* /v1/books/manipulation PUT - Change the name of the book with arguments (id) (NOTE: updated time should be changed as well)
* /v1/books/manipulation GET - Returns “No implementation for `GET` method”
* /v1/books/latest GET - Get all the latest added books limited by some amount with arguments (limit)
* /v1/books/info GET - Get info(type, name etc …) about a book with arguments (ID)
* /v1/books/ids GET - Get all ID of books by title with arguments (title)


### How to run application:

1. Install Docker
2. Clone this repository
3. Open terminal and navigate to cloned repository
4. Build docker image:
 > $ docker build -t python-flask-rest .
5. Run container:
 > $ docker run -p 127.0.0.1:5000:5000  python-flask-rest
 
The output will be like
  >GDSpb1331:~ sdronnikova$ docker run -p 127.0.0.1:5000:5000  python-flask-rest
 >* Serving Flask app "books_app.rest_api.flask_api" (lazy loading)
 >* Environment: production
 >  WARNING: This is a development server. Do not use it in a production deployment.
 >  Use a production WSGI server instead.
 >* Debug mode: on
 
 Example of request:
> $ curl http://127.0.0.1:5000/v1/books/latest?limit=1

 

