from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

# TODO: Write some tests (https://fastapi.tiangolo.com/tutorial/testing/)
"""
Tests to perform (also stress test and check for errors):
 - create N users
 - read all users
 - read particular user
 - update user
 - read particular user again
 - read all users again
 
 - create some roles
 - read all roles
 - read particular role
 - update role
 - read particular role
 - read all roles
 
 - add some roles to some users
 - remove some roles from some users
 
 - delete users / roles interchangeably
"""
