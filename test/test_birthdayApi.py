import pytest, requests 
from datetime import date, datetime, timedelta

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
    dob = today + timedelta(days=85)

    test = request_helper('PUT', DEFAULT_USER, dob.date().isoformat())
    assert 'cannot be in the future' in test[0]
    assert test[1] == 400

def test_put_dob_format():
    dob = '17-09-1998'

    test = request_helper('PUT', DEFAULT_USER, dob)
    assert 'Date format is incorrect' in test[0]
    assert test[1] == 400

### GET tests ###

def test_get_birthday_days():
    today = datetime.now()
    dob_increment = 105

    dob = today + timedelta(days=dob_increment)
    dob = dob.replace(year=1998)
    request_helper('PUT', DEFAULT_USER, dob.date().isoformat())

    test = request_helper('GET', DEFAULT_USER, None)
    assert f'Hello, {DEFAULT_USER}! Your birthday is in {dob_increment} day(s)' in test[0]
    assert test[1] == 200

def test_get_bday_today():
    today = datetime.now()
    dob = today.replace(year=2010)

    request_helper('PUT', DEFAULT_USER, dob.date().isoformat())

    test = request_helper('GET', DEFAULT_USER, None)
    assert f'Hello, {DEFAULT_USER}! Happy birthday!' in test[0]
    assert test[1] == 200

def test_get_user_not_found():
    user = 'randomUser'

    test = request_helper('GET', user, None)
    assert 'do not seem to have your date of birth' in test[0]
    assert test[1] == 404