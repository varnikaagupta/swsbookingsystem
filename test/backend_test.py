from atexit import register
import flask_sqlalchemy
import datetime
import sys
import os
sys.path.append(os.path.abspath("../models"))
from models import *

init_test()

def test_student_register():
    '''
    Testing student registration function
    '''
    user = {
        "email": "test@test.com",
        "password": "password",
        "first_name": "Bob",
        "last_name": "Lastname",
        "address": "address",
        "postal_code": "K7L 3N6",
        "date_of_birth": datetime.datetime(2000, 10, 3),
        "student_no": "66666666",
        "ohip": "012345678912",
        "sex": "M",
        "province": "ON",
        "perm_addr": "Perm Address",
        "faculty": "Engineering",
        "program": "Comp Eng",
        "year": "1",
        "degree_type": "Bachelor's",
        "domestic": True,
        "full_time": True
    }

    assert create_user(user) is not None


def test_login():
    user = {
        "email": "test1@test.com",
        "password": "password",
        "first_name": "Bob",
        "last_name": "Lastname",
        "address": "address",
        "postal_code": "K7L 3N6",
        "date_of_birth": datetime.datetime(2000, 10, 3),
        "student_no": "66666667",
        "ohip": "012345678913",
        "sex": "M",
        "province": "ON",
        "perm_addr": "Perm Address",
        "faculty": "Engineering",
        "program": "Comp Eng",
        "year": "1",
        "degree_type": "Bachelor's",
        "domestic": True,
        "full_time": True
    }
    user = create_user(user)
    assert login(user.email, user.password) is not None
