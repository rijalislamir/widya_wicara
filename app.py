from flaskapp import app, db

if __name__ == '__main__':
    # Initiate database
    db.create_all()

    # Run flask app
    app.run(debug=True)
