from curses.ascii import isalpha
from flask import Flask, jsonify, request
import boto3
from datetime import datetime
from markupsafe import escape
import os
from boto3.dynamodb.conditions import Key

# Temporary method for local Store
#DB_DICT = {}
TABLE_NAME = 'user-records'
DDB_URL = os.environ['DYNAMO_URL']
DDB_PORT = os.environ['DYNAMO_PORT']
REGION = os.environ['AWS_REGION']

db = boto3.resource('dynamodb', endpoint_url=f'http://{DDB_URL}:{DDB_PORT}', region_name='eu-west-1')
table = db.Table(TABLE_NAME)

class User:
    def __init__(self, username, dob):
        self.username = username
        self.dob = dob

    @classmethod
    def fromString(cls, username, dob_string):
        dob = datetime.strptime(dob_string, '%Y-%m-%d')

        if dob.date() < datetime.now().date():
            return cls(username, dob)
        else:
            raise Exception('Date of birth cannot be in the future')

    @classmethod
    # For use when loading from DB
    def fromIsoformat(cls, username, dob_iso):
        return cls(username, datetime.fromisoformat(dob_iso))

    def toDict(self):
        return {'username': self.username, 'date.of.birth': self.dob.isoformat()}

    def daysToBday(self):
        today = datetime.now()
        cur_year = today.year
        temp_bday = self.dob.replace(year=cur_year) # Only the day & month are of interest

        if today.date() > temp_bday.date():
            # User has already had their birthday this year, calc days until next
            temp_bday = self.dob.replace(year=(cur_year+1))

        bday_delta = temp_bday.date() - today.date()
        return bday_delta.days



app = Flask(__name__)


@app.route('/hello/<username>', methods=['PUT'])
def updateUser(username):
    if not username.isalpha():
        msg = {"message":"Username must only contain letters"}
        statusCode = 400
        return jsonify(msg), statusCode

    usr_input = escape(request.json['dateOfBirth'])
    
    try:
        usr = User.fromString(username, str(usr_input))
        db_write(usr)
        msg = ""
        statusCode = 204
    except ValueError as e:
        print(e)
        if 'does not match format' in str(e):
            msg = {"message":"Date format is incorrect, please use the format YYYY-MM-DD"}
            statusCode = 400
    except Exception as e:
        print(e)
        msg = {"message":"Date of birth cannot be in the future"}
        statusCode = 400
    return jsonify(msg), statusCode

@app.route('/hello/<username>', methods=['GET'])
def getBirthday(username):
    username = escape(username)
    clean_usr = str(username)
    try:
        usr_obj = db_read(clean_usr)
        bday_delta = usr_obj.daysToBday()
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
# def db_write(user: User):
#     usr_dict = user.toDict()
#     DB_DICT[(usr_dict['username'])] = usr_dict['dob']
    
# def db_read(username) -> User:
#     if username in DB_DICT:
#         return User.fromIsoformat(username, DB_DICT[username])
#     else:
#         raise KeyError(f'User {username} not found in the DB')


def db_write(user: User):
    usr_dict = user.toDict()
    table.put_item(Item=usr_dict)
    
def db_read(username) -> User:
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    usr_data = response['Items']

    if usr_data:
        return User.fromIsoformat(username, usr_data[0]['date.of.birth'])
    else:
        raise KeyError(f'User {username} not found in the DB')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)