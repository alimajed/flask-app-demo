from ma import ma
from models.movies import MovieModel
 
 
class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MovieModel
        dump_only = ("id",)
        load_instance = True