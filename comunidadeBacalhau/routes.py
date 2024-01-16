import os
import secrets
from PIL import Image as Image

from flask import render_template, flash, redirect, url_for, request, abort
from comunidadeBacalhau import app, database, bcrypt
from comunidadeBacalhau.forms import (FormLogin, FormCriarConta, FormEditprofile, FormCreatePost, FormEditPost,
                                      FormCreateCourse, FormEditCourse, FormResetPassword, FormSearch)
from comunidadeBacalhau.models import User, Post, Course
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/login/", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_password.data)
            flash(
                f'Login feito com sucesso no e-mail: {form_login.email.data}', 'notification is-success')
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for("home")
            return redirect(next_page)
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos',
                'notification is-danger')
    return render_template("login.html", form_login=form_login)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        # criando o hash da senha
        password_hash = bcrypt.generate_password_hash(
            form_criarconta.password.data)
        # criando um novo usuário
        user = User(username=form_criarconta.username.data,
                    email=form_criarconta.email.data,
                    password=password_hash)
        # adicionando usuario no banco de dados
        database.session.add(user)
        database.session.commit()
        flash(
            f'Conta criada com sucesso!: {form_criarconta.username.data}', 'notification is-success')
        return redirect(url_for("login"))
    return render_template("signup.html", form_criarconta=form_criarconta)


# PAGE HOME
@app.route("/")
@app.route("/home/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=2)
    
    return render_template("home.html", posts=posts)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('Logout feito! Bye Bye...', 'notification is-warning')
    return redirect(url_for("home"))


@app.route("/users/")
@login_required
def users():
    list_users = User.query.all()
    profile_picture = url_for(
        'static', filename='fotos_perfil/{}'.format(current_user.profile_picture))
    return render_template("users.html", list_users=list_users, profile_picture=profile_picture)


@app.route("/profile/")
@login_required
def profile():
    profile_picture = url_for(
        'static', filename='fotos_perfil/{}'.format(current_user.profile_picture))
    return render_template('profile.html', profile_picture=profile_picture)


# function save_picture to save the profile picture
# thumbnail to resize the image
# save the image in the static folder
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/fotos_perfil', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/edit_profile/", methods=["GET", "POST"])
@login_required
def edit_profile():
    form_edit_profile = FormEditprofile()
    if form_edit_profile.validate_on_submit():
        current_user.username = form_edit_profile.username.data
        current_user.email = form_edit_profile.email.data
        # fazendo o upload do foto-perfil
        if form_edit_profile.profile_picture.data:
            profile_picture = save_picture(
                form_edit_profile.profile_picture.data)
            current_user.profile_picture = profile_picture
        # atualizando os dados no banco de dados
        database.session.commit()
        flash('Profile updated successfully!', 'notification is-success')
        return redirect(url_for('profile'))
        # preenchendo os campos com os dados do usuário
    elif request.method == 'GET':
        form_edit_profile.username.data = current_user.username
        form_edit_profile.email.data = current_user.email
    profile_picture = url_for(
        'static', filename='fotos_perfil/{}'.format(current_user.profile_picture))
    return render_template("edit_profile.html", form_edit_profile=form_edit_profile, profile_picture=profile_picture)


# criar post
@app.route("/create_post/", methods=["GET", "POST"])
@login_required
def create_post():
    form_post = FormCreatePost()
    if form_post.validate_on_submit():
        post = Post(title=form_post.title.data,
                    content=form_post.content.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post created successfully!', 'notification is-success')
        return redirect(url_for('home'))
    return render_template("create_post.html", form_post=form_post)


# exibir o post
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def display_post(post_id):
    post = Post.query.get_or_404(post_id)
    form_edit = FormEditPost()
    if  request.method == 'GET':
        form_edit.title.data = post.title
        form_edit.content.data = post.content
    elif form_edit.validate_on_submit():
        post.title = form_edit.title.data
        post.content = form_edit.content.data
        database.session.commit()
        flash('Post updated successfully!', 'notification is-success')
        return redirect(url_for('display_post', post_id=post.id))
    else:
        form_edit = None
    
    return render_template("post.html", post=post, form_edit=form_edit)
    
    
    
@app.route("/results/<string:search>", methods=["GET", "POST"])
def result(search):
    posts = Post.query.filter(Post.title.contains(search) | Post.content.contains(search)).all()
    for_search = FormSearch()
    if request.method == 'GET':
        for_search.search.data = search
    elif for_search.validate_on_submit():
        return redirect(url_for('result', search=for_search.search.data))
    else:
        for_search = None
        
    return render_template("results.html", posts=posts, for_search=for_search)
    
    

# deletar o post
@app.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post deleted successfully!', 'notification is-warning')
        return redirect(url_for('home'))
    else:
        abort(403)
        


@app.route("/courses/")
@login_required
def courses():
    return render_template("courses.html", courses="courses")


@app.route("/create_course/", methods=["GET", "POST"])
@login_required
def create_course():
    return render_template("create_course.html", create_course="create_course")


@app.route("/edit_course/")
@login_required
def edit_course():
    return render_template("edit_course.html", edit_course="edit_course")


@app.route("/delete_course/")
@login_required
def delete_course():
    return render_template("delete_course.html", delete_course="delete_course")


@app.route("/about/")
def about():
    return render_template("about.html", about="about")


@app.route("/contact/")
def contact():
    return render_template("contact.html", contact="contact")
