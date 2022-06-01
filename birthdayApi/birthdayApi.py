from flask import Flask, jsonify

app = Flask(__name__)

user = 'test_user'
dob = '12/04/1993'

@app.route('/')
def dob_test():
    temp_dict = {}
    temp_dict['message'] = f'Hello {user}, your bday is {dob}'

    return jsonify(temp_dict)