from comunidadeBacalhau import app, database

with app.app_context():
    database.create_all()