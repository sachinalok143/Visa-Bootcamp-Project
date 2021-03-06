from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dkaalsgsvycdnw:b12fae3ad33a83367352a4b72ef8e5843703134eeaada07ef5' \
                                        'dc890850b5b74b@ec2-54-160-202-3.compute-1.amazonaws.com:5432/d5ou4mml7frs0o'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    username = db.Column('username', db.Text, primary_key=True)
    password = db.Column('password', db.Text)


class User(db.Model):
    __tablename__ = 'user'
    username = db.Column('username', db.Text, primary_key=True)
    email = db.Column('email', db.Text)
    fname = db.Column('fname', db.Text)
    lname = db.Column('lname', db.Text)
    points = db.Column('points', db.Integer)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET'])
def login():
    request_body = request.get_json()
    user_credentials = UserCredentials.query.get(request_body['username'])

    response = dict()
    if user_credentials is not None:
        if user_credentials.password == request_body['password']:
            response['status'] = 'SUCCESS'
        else:
            response['status'] = 'INCORRECT_PASSWORD'
    else:
        response['status'] = 'INCORRECT_USERNAME'

    return json.dumps(response)


@app.route('/user', methods=['GET'])
def get_user_details():
    request_body = request.get_json()
    user_details = User.query.get(request_body['username'])
    response = dict()
    if user_details is not None:
        response['status'] = 'SUCCESS'
        user_details_dict = user_details.__dict__
        _ = user_details_dict.pop('_sa_instance_state')
        response['response'] = user_details_dict
    else:
        response['status'] = 'INCORRECT_USERNAME'

    return json.dumps(response)


if __name__ == '__main__':
    app.run()
