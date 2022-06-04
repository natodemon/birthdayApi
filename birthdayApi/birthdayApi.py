from flask import Flask, jsonify
import boto3
from datetime import datetime, timedelta

# Temporary method for local Store
DB_DICT = {}

class User:
    def __init__(self, username, dob):
        self.username = username
        self.dob = dob

    @classmethod
    def fromString(cls, username, dob_string):
        return cls(username, datetime.strptime(dob_string, '%Y-%m-%d'))

    @classmethod
    def fromIsoformat(cls, username, dob_iso):
        return cls(username, datetime.fromisoformat(dob_iso))

    def toDict():
        return {'username': '{self.username}', 'dob': '{self.dob.isoformat}'}

app = Flask(__name__)
db = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

user = 'test_user'
dob = '12/04/1993'

@app.route('/')
def dob_test():
    temp_dict = {}
    temp_dict['message'] = f'Hello {user}, your bday is {dob}'

    return jsonify(temp_dict)


# Temporary methods for local key-value store
def db_write(user: User):
    usr_dict = user.toDict()
    DB_DICT[usr_dict['username']] = usr_dict['dob']
    
def db_read(username) -> User:
    return User.fromIsoformat(username, DB_DICT[username])