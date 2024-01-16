from comunidadeBacalhau import database, login_manager
from datetime import datetime
from flask_login import UserMixin


# function para encontrar o usuario pelo id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(40), nullable=False)
    email = database.Column(database.String(40), unique=True, nullable=False)
    password = database.Column(database.String(40), nullable=False)
    profile_picture = database.Column(database.String(40), default="default.jpg", nullable=False)
    courses = database.Column(database.String(40), nullable=False, default="Não Informado")
    
    def count_posts(self):
        return len(self.posts)
    
    
    def count_courses(self):
        return len(self.courses)
    


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    content = database.Column(database.Text, nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
    author_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
    author = database.relationship("User", backref="posts", lazy=True)


class Course(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    description = database.Column(database.Text, nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
    instructor_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
    instructor = database.relationship("User", backref="authors", lazy=True)
