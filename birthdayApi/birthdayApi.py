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

    def toDict(self):
        return {'username': self.username, 'dob': self.dob.isoformat()}

    def daysToBday(self, today):
        cur_year = today.year
        temp_bday = self.dob.replace(year=cur_year)

        if today.date() > temp_bday.date():
            temp_bday = self.dob.replace(year=(cur_year+1))

        bday_delta = temp_bday.date() - today.date()
        return bday_delta.days



app = Flask(__name__)
#db = boto3.client('dynamodb', endpoint_url='http://localhost:8000')


@app.route('/hello/<username>', methods=['PUT'])
def updateUser(username):
    username = escape(username)
    clean_usr = str(username) # Replace w/ escape(username) to string
    usr_input = request.json
    usr = User.fromString(clean_usr, usr_input['dateOfBirth'])
    db_write(usr)
    print(f'You have added the username {clean_usr} with dob {usr_input["dateOfBirth"]}')
    print(f'Dict keys are: {usr.toDict()}')
    return "", 204

@app.route('/hello/<username>', methods=['GET'])
def getBirthday(username):
    username = escape(username)
    clean_usr = str(username) # Fix this
    try:
        usr_obj = db_read(clean_usr)
        bday_delta = usr_obj.daysToBday(datetime.now())
        if bday_delta < 1:
            msg = {"message": f"Hello, {clean_usr}! Happy birthday!"}
        else:
            msg = {"message": f"Hello, {clean_usr}! Your birthday is in {bday_delta} day(s)"}
        statusCode = 200
    except KeyError:
        msg = {"message": f"Hello {clean_usr}, we do not seem to have your date of birth on record"}
        statusCode = 404
    return jsonify(msg), statusCode



# Temporary methods for local key-value store
def db_write(user: User):
    usr_dict = user.toDict()
    DB_DICT[(usr_dict['username'])] = usr_dict['dob']
    
def db_read(username) -> User:
    if username in DB_DICT:
        return User.fromIsoformat(username, DB_DICT[username])
    else:
        raise KeyError(f'User {username} not found in the DB')