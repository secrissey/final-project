from catsapp_api import app, db, ma, login_manager

from datetime import datetime

import uuid

from flask_login import UserMixin

# Import for Werkzeug Security
from werkzeug.security import generate_password_hash, check_password_hash

class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable = False)
    user_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

    def __init__(self,full_name, user_name, email, id = id):
        self.full_name = full_name
        self.user_name = user_name
        self.email = email

        def __repr__(self):
            return f'Member {self.full_name} has been added to the database.'



class MemberSchema(ma.Schema):
    class Meta:
        # Fields to show in output
        fields = ["id","full_name","user_name","email"]

member_schema = MemberSchema()
members_schema = MemberSchema(many = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token = db.Column(db.String(400))
    token_refreshed = db.Column(db.Boolean, default = False)
    date_refreshed = db.Column(db.DateTime)

    def __init__(self,name,email,password,id = id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = self.set_password(password)

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'{self.name} has been created successfully'


# Creation of the Post Model
# The Post model will have: id,title,content,date_created,user_id
class Post(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable = False)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f'The title of the post is {self.title} \n and the content is {self.content}'