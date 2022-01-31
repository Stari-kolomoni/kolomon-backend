from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

# TODO: Write some tests (https://fastapi.tiangolo.com/tutorial/testing/)
"""
Tests to perform (also test and check for errors):
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


def test_create_users():
    response_gorazd = client.post(
        "/users/",
        json={
            'username': 'gorazd',
            'display_name': 'Gorazd',
            'password': 'geslo123'
        }
    )

    response_simon = client.post(
        "/users/",
        json={
            'username': 'Simon',
            'password': 'geslo123'
        }
    )

    response_cefizelj = client.post(
        "/users/",
        json={
            'display_name': 'Cefizelj',
            'password': 'geslo123'
        }
    )

    response_klepec = client.post(
        "/users/",
        json={
            'username': 'peterK'
        }
    )

    response_krpan = client.post(
        "/users/",
        json={
            'name': 'krpan77',
            'password': 'geslo123'
        }
    )

    response_impostor = client.post(
        "/users/",
        json={
            'username': 'gorazd',
            'password': 'geslo123'
        }
    )

    assert response_gorazd.status_code == 200
    assert response_simon.status_code == 200
    assert response_cefizelj.status_code == 422
    assert response_klepec.status_code == 422
    assert response_krpan.status_code == 422
    assert response_impostor.status_code == 400


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': int,
            'username': 'gorazd',
            'display_name': 'Gorazd',
            'is_active': False
        },
        {
            'id': int,
            'username': 'Simon',
            'display_name': None,
            'is_active': False
        }
    ]


