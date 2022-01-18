from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskapp import app, db
from flaskapp.forms import MovieForm, SearchForm
from flaskapp.models import Movie, Genre, MovieSchema
from pathlib import Path
import json

@app.route("/")
def home():
    """Generate all movies object

    Returns:
        Render home template
    """
    # Get page from URL parameter
    page = request.args.get('page', 1, type=int)

    # Get movies object by specific page
    movies = Movie.query.order_by(Movie.id.desc()).paginate(page=page, per_page=5)

    # Render template
    return render_template('home.html', movies=movies)

@app.route("/movie/new", methods=['GET', 'POST'])
def create_movie():
    """Create new movies

    Fill in the inputs to create a new movie object. 
    A Genre that has never been entered, will be created into a new object.

    Returns:
        Redirect to home route if MovieForm is submitted or render create template
    """
    # Create instance of MovieForm
    form = MovieForm()

    # Enter conditional When form is submitted
    if form.validate_on_submit():
        genres = []

        # Process string genres to be list
        raw_genres = [x.strip() for x in form.genres.data.split(',')]
        
        for genre in raw_genres:
            # Search genre by name
            genre_obj = Genre.query.filter(Genre.name.like(genre)).first()

            # If find any genre object
            if genre_obj:
                # Add the id of genre object
                genres.append(genre_obj)
            # If dont find any
            else:
                # Create new genre object
                new_genre = Genre(name=genre)
                db.session.add(new_genre)
                db.session.commit()

                # Add the id of genre object
                genres.append(new_genre)

        # Create new movie object
        movie = Movie(
            title=form.title.data,
            genres=genres,
            rating=form.rating.data,
            duration=form.duration.data,
            quality=form.quality.data,
            trailer=form.trailer.data,
            watch=form.watch.data,
        )
        db.session.add(movie)
        db.session.commit()

        # Add success notification of creating movie object
        flash(f'{form.title.data} movie has been listed!', 'success')

        # Redirect to home route
        return redirect(url_for('home'))

    # Render template
    return render_template('create.html', title='New Movie', form=form)

@app.route("/movie/<int:movie_id>/delete", methods=['POST'])
def delete_movie(movie_id):
    """Delete selected movie from the database

    Returns:
        Redirect to home route
    """
    # Select movie object by id
    movie = Movie.query.get_or_404(movie_id)
    
    # Save the title for showing notification
    title = movie.title
    
    db.session.delete(movie)
    db.session.commit()

    # Add success notification of deleting movie object
    flash(f"{title} has been deleted!", "success")

    # Redirect to home route
    return redirect(url_for('home'))

# This fuunction was created for solving error on adding "form.hidden_tag()" function in layout.html
@app.context_processor
def base():
    # Create instance of SearchForm
    form = SearchForm()

    return dict(form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    """Search movies based on the title

    Generate objects of movies that the title is similar to a given query.

    Returns:
        Render search template
    """
    # Create instance of SearchForm
    form = SearchForm()

    # Get parameter from URL
    page = request.args.get('page', 1, type=int)
    q = request.args.get('query', '', type=str)

    # Enter conditional When form is submitted
    query = form.searched.data if form.validate_on_submit() else q

    # Filter movies by title-like
    movies = Movie.query.filter(Movie.title.like('%' + query  + '%'))

    # Order the filtered movies
    movies = movies.order_by(Movie.title).paginate(page=page)

    # Add success notification of searching movie object
    flash(f'Found {movies.total} movies for "{query}" keyword!', 'success')

    # Render template
    return render_template('search.html', title=f'Results for "{query}"', movies=movies, query=query)

@app.route("/export")
def export_movie():
    """Export movie from database to JSON file

    Generally, an object of class cannot be converted to JSON directly, because the object
    is not serializable. So the thing to do is convert the object to become serializable.
    And after that, we can return the JSON file.

    Returns:
        JSON file
    """
    # Get all movie objects
    movies = Movie.query.all()

    # Instantiate MovieSchema
    movie_schema = MovieSchema(many=True)

    # Serialaze movie objects
    output = movie_schema.dump(movies)

    # Return output with JSON structure
    return jsonify({'data': output})

@app.route("/import-dummy", methods=['POST'])
def import_dummy():
    """Import provided dummy data from dummy.json

    Fill the database with dummy data and replace the existing data in database. 
    The first thing to do is delete all tables from the database. After that create
    the new one based on models. And then open dummy.json file to create a new movie object
    through the loop.

    Returns:
        Redirect to home route
    """
    # Drop all table
    db.drop_all()

    # Create all table based on models.py
    db.create_all()

    # Open file dummy.json
    file_to_open = Path("flaskapp/dummy.json")
    with open(file_to_open) as json_file:
        # Convert json to be dictionary
        movies_dict = json.load(json_file)["data"]
        movies = []

        for movie in movies_dict:
            # Initiate and reset genre
            genres = []

            # Collecting genres for each movie
            for genre in movie["genre"]:
                # Search genre by name
                genre_obj = Genre.query.filter(Genre.name.like(genre)).first()

                # If find any genre object
                if genre_obj:
                    # Add the id of genre object
                    genres.append(genre_obj)
                # If dont find any
                else:
                    # Create new genre object
                    new_genre = Genre(name=genre)
                    db.session.add(new_genre)
                    db.session.commit()

                    # Add the id of genre object
                    genres.append(new_genre)

            # Create new instance for movie object
            new_movie = Movie(
                title=movie.get("title"),
                genres=genres,
                rating=movie.get("rating"),
                duration=movie.get("duration"),
                quality=movie.get("quality"),
                trailer=movie.get("trailer"),
                watch=movie.get("watch"),
            )

            # Collect movie object
            movies.append(new_movie)
        
        # Add all created movie object to database
        if movies:
            db.session.add_all(movies)
            db.session.commit()

    # Add success notification of importing dummy data to movie object
    flash(f'{len(movies_dict)} dummy data has been imported!', 'success')

    # Render template
    return redirect(url_for('home'))
