from flask import Flask, jsonify
import boto3
from datetime import datetime, timedelta


DB_DICT = {}

class User:
    def __init__(self, username, dob):
        self.username = username
        self.dob = dob

    @classmethod
    def fromString(cls, username, dob_string):
        return cls(username, datetime.strptime(dob_string, '%Y-%m-%d'))

app = Flask(__name__)
db = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

user = 'test_user'
dob = '12/04/1993'

@app.route('/')
def dob_test():
    temp_dict = {}
    temp_dict['message'] = f'Hello {user}, your bday is {dob}'

    return jsonify(temp_dict)

def db_write(user: User):
    d
def db_read() -> User:
    a