from flask import Flask, jsonify
from flask_restful import Api
from db import db
from ma import ma
from resources.movies import Movie, MovieCreate, MovieUpload, MoviesList, MoviesDownload


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Movie, "/movie/<string:name>")
api.add_resource(MovieCreate, "/movie")
api.add_resource(MovieUpload, "/movie/upload")
api.add_resource(MoviesList, "/movies/list/<int:page>/<int:page_size>")
api.add_resource(MoviesDownload, "/movies/download/<string:file_name>")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
