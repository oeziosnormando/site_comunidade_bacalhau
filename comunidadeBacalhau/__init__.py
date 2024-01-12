from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "9546c47c883eb1bd5a6ae69301399f6f"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidadeBacalhau.db"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Por gentileza! Faça login para acessar esta página"
login_manager.login_message_category = "notification is-warning"


from comunidadeBacalhau import routes


    
