import pytest, requests 
from datetime import datetime, timedelta

## Insert here commands to startup docker

DEFAULT_USER = 'test'
DEFAULT_DOB = '1998-09-17'

def request_helper(req_type, username, dateOfBirth):
    if req_type == 'PUT':
        req = requests.put(f'http://localhost:5000/hello/{username}', json={"dateOfBirth": dateOfBirth})
    elif req_type == 'GET':
        req = requests.get(f'http://localhost:5000/hello/{username}')

    return req.text, req.status_code


def test_put_response_code():
    test = request_helper('PUT', DEFAULT_USER, DEFAULT_DOB)
    assert test[1] == 204

def test_put_bad_user():
    user = 'test1'

    test = request_helper('PUT', user, DEFAULT_DOB)
    assert 'only contain letters' in test[0]
    assert test[1] == 400

def test_put_future_dob():
    today = datetime.now()
    increment = timedelta(days=85)
    dob = today + increment

    test = request_helper('PUT', DEFAULT_USER, dob.date().isoformat())
    assert 'cannot be in the future' in test[0]
    assert test[1] == 400