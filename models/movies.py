from db import db
from typing import List

class MovieModel(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    director = db.Column(db.String(80), nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save_to_db_multiple(cls, movies: List["MovieModel"]) -> None:
        db.session.add(movies)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "MovieModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls, page=0, page_size=None) -> List["MovieModel"]:
        query =  cls.query
        if page_size:
            query = query.limit(page_size)
        if page: 
            query = query.offset(page*page_size)
        return query.all()