from flask import Flask, jsonify, request
import boto3
from datetime import datetime, timedelta
from markupsafe import escape

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

    def daysToBday(todayDate):
        print()
        # Strip 
        


app = Flask(__name__)
#db = boto3.client('dynamodb', endpoint_url='http://localhost:8000')


@app.route('/hello/<username>', methods=['PUT'])
def updateUser(username):
    clean_usr = username # Replace w/ escape(username) to string
    usr_input = request.json
    usr = User.fromString(clean_usr, usr_input["dateOfBirth"])
    db_write(usr)
    print(f'You have added the username {clean_usr} with dob {usr_input["dateOfBirth"]}')
    return "", 204

@app.route('/hello/<username>', methods=['GET'])
def getBirthday(username):
    clean_usr = username # Fix this
    usr_obj = db_read(clean_usr)


# Temporary methods for local key-value store
def db_write(user: User):
    usr_dict = user.toDict()
    DB_DICT[usr_dict['username']] = usr_dict['dob']
    
def db_read(username) -> User:
    return User.fromIsoformat(username, DB_DICT[username])