from flaskapp import db, ma

movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    genres = db.relationship('Genre', secondary=movie_genre, backref='movies')
    rating = db.Column(db.String, nullable=True)
    duration = db.Column(db.String(), nullable=True)
    quality = db.Column(db.String(), nullable=True)
    trailer = db.Column(db.String(), nullable=True)
    watch = db.Column(db.String(), nullable=True)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
