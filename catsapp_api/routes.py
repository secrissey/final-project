from catsapp_api import app, db
from catsapp_api.models import Member, member_schema, members_schema, User, Post, check_password_hash
from flask import jsonify, request, render_template, redirect, url_for

# Import for Flask Login 
from flask_login import login_required, login_user, current_user, logout_user

# Import for PyJWT (Json Web Token)
import jwt

from catsapp_api.forms import UserForm, LoginForm, PostForm

from catsapp_api.token_verification import token_required

# Endpoint for Creating members
@app.route('/members/create', methods = ['POST'])
@token_required
def create_member(current_user_token):
    name = request.json['full_name']
    email = request.json['email']

    member = Member(name,email)
    results = member_schema.dump(member)
    return jsonify(results)

# Endpoint for All Members
@app.route('/members', methods = ['GET'])
@token_required
def get_members(current_user_token):
    members = Member.query.all()
    return jsonify(members_schema.dump(members))
    

# Endpoint for ONE member based on their ID
@app.route('/members/<id>', methods = ['GET'])
@token_required
def get_member(current_user_token,id):
    member = Member.query.get(id)
    results = member_schema.dump(member)
    return jsonify(results)

# Endpoint for updating member data
@app.route('/members/<id>', methods = ['POST', 'PUT'])
@token_required
def update_member(current_user_token,id):
    member = Member.query.get(id)
    
    member.name = request.json['full_name']
    member.email = request.json['email']

    db.session.commit()

    return member_schema.jsonify(member)

# Endpoint for deleting member data
@app.route('/members/delete/<id>', methods = ['DELETE'])
@token_required
def delete_member(current_user_token,id):
    member = Member.query.get(int(id))
    db.session.delete(member)
    db.session.commit()
    result = member_schema.dump(member)
    return jsonify(result)


@app.route('/')
def home():
    return render_template('home.html', user_posts = posts)

@app.route('/users/register', methods = ['GET','POST'])
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(name,email,password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', user_form = form)



@app.route('/users/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        login_user(logged_user)
        return redirect(url_for('main'))
    return render_template('login.html', login_form = form)


@app.route('/main')
def main():
   # posts = Post.query.all()
    return render_template('main.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Creation of posts route(aka Crud Process)
@app.route('/posts', methods = ['GET', 'POST'])
@login_required
def posts():
    form = PostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        post = Post(title,content,user_id)

        db.session.add(post)

        db.session.commit()
        return redirect(url_for('main'))
    return render_template('posts.html', post_form = form)

# post detail route to display info about a post
@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post = post)

@app.route('/posts/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id

        # Update the Database with the new Info
        post.title = title
        post.content = content
        post.user_id = user_id

        # Commit the changes to the Database
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('post_update.html', update_form = form)

@app.route('/posts/delete/<int:post_id>', methods = ['GET','POST','DELETE'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/users/getkey', methods = ['GET'])
def get_key():
    token = jwt.encode({'public_id': current_user.id, 'email': current_user.email}, app.config['SECRET_KEY'])
    user = User.query.filter_by(email = current_user.email).first()
    user.token = token

    db.session.add(user)
    db.session.commit()
    results = token.decode('utf-8')
    return render_template('token.html', token = results)

# Get a new API KEY
@app.route('/users/updatekey', methods = ['GET', 'POST', 'PUT'])
def refresh_key():
    refresh_key = {'refreshToken': jwt.encode({'public_id': current_user.id, 'email': current_user.email}, app.config['SECRET_KEY'])}
    temp = refresh_key.get('refreshToken')
    new_token = temp.decode('utf-8')

    # Adding Rereshed Token to DB
    user = User.query.filter_by(email = current_user.email).first()
    user.token = new_token

    db.session.add(user)
    db.session.commit()
    
    return render_template('token_refresh.html', new_token = new_token)
