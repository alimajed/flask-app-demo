from flask import request, render_template, send_file
from flask_restful import Resource
from models.movies import MovieModel
from schemas.movies import MovieSchema
from helpers.randoms import randomstr
import pandas as pd
import numpy as np
import pdfkit

NAME_ALREADY_EXISTS = "A movie with name '{}' already exists."
NAME_ALREADY_EXISTS_MULTIPLE = "movies with name '{}' already exist."
ERROR_INSERTING = "An error occurred while inserting the movie."
MOVIE_NOT_FOUND = "Movie not found."
NO_FILE_PART = "No file part"
NO_FILE_UPLOADED = "No selected file"
FILE_EXTENSION_ERROR = "Uploaded file extension not allowed and may cause process failure"

movie_schema = MovieSchema()
movies_list_schema = MovieSchema(many=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

class Movie(Resource):
    @classmethod
    def get(cls, name: str):
        movie = MovieModel.find_by_name(name)
        if movie:
            return movie_schema.dump(movie), 200

        return {"message": MOVIE_NOT_FOUND}, 404


class MovieCreate(Resource):
    @classmethod
    def post(cls):
        movie_json = request.get_json()
        if MovieModel.find_by_name(movie_json["name"]):
            return {"message": NAME_ALREADY_EXISTS.format(movie_json["name"])}, 400

        # movie_json["name"] = name
        # movie_json["director"] = director

        movie = movie_schema.load(movie_json)

        try:
            movie.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return movie_schema.dump(movie), 201


class MovieUpload(Resource):
    @classmethod
    def post(cls):
        # check if file uploaded
        if 'file' not in request.files:
            return {"message": NO_FILE_PART}, 400

        file = request.files['file']

        # check if file selected
        if file.filename == '':
            return {"message": NO_FILE_UPLOADED}, 400
        
        if '.' in file.name and file.name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            return {"message": FILE_EXTENSION_ERROR}, 400

        df = pd.read_excel(file)
        # remove nan object from data to prevent 'Not a valid string' throwed by marhmallow dump function
        df.replace(np.nan, '', regex=True, inplace=True)
        existed = []
        movies_list = []
        for index, row in df.iterrows():
            if MovieModel.find_by_name(row["Movies"]):
                existed.append(row["Movies"])
            else:
                movies_list.append({"name": row["Movies"], "director": row["Directors"] if row["Directors"] is not None else ''})
        
        if len(existed) > 0:
             return {"message": NAME_ALREADY_EXISTS.format(','.join(existed))}, 400
        
        for movie_item in movies_list:
            movie = movie_schema.load(movie_item)
            movie.save_to_db()
        return {"message": "File Uploaded"}, 200

class MoviesList(Resource):
    @classmethod
    def get(cls, page=0, page_size=None):
        result =  movies_list_schema.dump(MovieModel.find_all(page, page_size))
        if len(result) == 0:
            return {"message": "no data available"}, 200
        file_name = f"{randomstr(10)}"
        pdfkit.from_string(render_template("movies_list.html",movies = result), f'docs/{file_name}.pdf')
        return {"message": f"click on the link http://{request.host}/movies/download/{file_name}.pdf"}, 200

class MoviesDownload(Resource):
    @classmethod
    def get(cls, file_name: str):
        path = f"docs/{file_name}"
        return send_file(path, as_attachment=True)