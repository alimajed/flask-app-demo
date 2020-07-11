# Flask Task 2020-11-07

Using Flask to build a Restful API to upload excels sheet taht contains movies info and save it to the Database.
Integration with Flask-restful, Flask-SQLalchemy, pandas, pdfkit extensions.


## Extension:
- Restful: [Flask-restful](https://flask-restful.readthedocs.io/en/latest/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

- Execl sheet: [Pandas](https://pandas.pydata.org/)

- PDF files generation: [pdfkit](https://pdfkit.org/)


## Installation

Install with pip:

```
$ pip install -r requirements.txt
```


## Flask Configuration

### Example
```
app = Flask(__name__)
api = Api(app)
```

### Database Configuration
```
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
```

#### Create Database Automatically if not created
```
@app.before_first_request
def create_tables():
    db.create_all()
```

 
## Run Flask
### Run flask for develop
```
$ python app.py
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/`

#### upload route 
```
http://127.0.0.1:5000/movie/upload 

file in body as form data 
```

#### generate pdf route
```
http://127.0.0.1:5000/movies/list/{page}/{page_size}/

return link to download generated pdf file
```
