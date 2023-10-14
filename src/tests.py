import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# запустить тесты можно в терминале контейнера командой `pytest tests.py` в пустой бд

# city tests

def test_get_empty():
    response = client.get("/api/cities")
    assert response.status_code == 200
    obj = response.json()
    assert obj == []

def test_create_city1():
    response = client.post("/api/cities/?name=Tyumen")
    assert response.status_code == 200
    obj = response.json()
    assert obj['id'] == 1 and obj['name'] == "Tyumen"

def test_create_city2():
    response = client.post("/api/cities/?name=Helsinki")
    assert response.status_code == 200
    obj = response.json()
    assert obj['id'] == 2 and obj['name'] == "Helsinki"

def test_create_city2_lowercase():
    response = client.post("/api/cities/?name=helsinki")
    assert response.status_code == 200
    obj = response.json()
    assert obj['id'] == 2 and obj['name'] == "Helsinki"

def test_create_city3_error():
    response = client.post("/api/cities/?name=barzil")
    assert response.status_code == 404

def test_create_nofield():
    response = client.post("/api/cities/")
    assert response.status_code == 422

def test_create_city3():
    response = client.post("/api/cities/?name=bRaZIl")
    assert response.status_code == 200
    obj = response.json()
    assert obj['id'] == 3 and obj['name'] == "Brazil"

def test_get():
    response = client.get("/api/cities/")
    assert response.status_code == 200
    obj = response.json()
    assert any(dictionary.get('name') == 'Tyumen' for dictionary in obj) and \
           any(dictionary.get('name') == 'Helsinki' for dictionary in obj) and \
           any(dictionary.get('name') == 'Brazil' for dictionary in obj)
    
def test_get_city3():
    response = client.get("/api/cities/?name=helsinki")
    assert response.status_code == 200
    obj = response.json()
    assert any(dictionary.get('name') == 'Helsinki' for dictionary in obj)

def test_get_city3_wrongfilter():
    response = client.get("/api/cities/?name=helsnki")
    assert response.status_code == 200
    obj = response.json()
    assert obj == []

# user tests

def test_get_empty_userlist():
    response = client.get("/api/users/")
    assert response.status_code == 200
    obj = response.json()
    assert obj == []

def test_create_user1():
    response = client.post("/api/users/", json={'name': 'Bob', 'surname': 'Johnson', 'age': 27})
    assert response.status_code == 200
    obj = response.json()
    assert obj == {'id': 1, 'name': 'Bob', 'surname': 'Johnson', 'age': 27}

def test_create_user_nofield():
    response = client.post("/api/users/")
    assert response.status_code == 422

def test_create_user2_nofield():
    response = client.post("/api/users/", json={'name': 'John', 'age': 45})
    assert response.status_code == 422

def test_create_user2():
    response = client.post("/api/users/", json={'age': 45, 'name': 'John', 'surname': 'Bobson'})
    assert response.status_code == 200
    obj = response.json()
    assert obj == {'id': 2, 'name': 'John', 'surname': 'Bobson', 'age': 45}

def test_create_user3():
    response = client.post("/api/users/", json={'age': 86, 'name': 'Old', 'surname': 'Man'})
    assert response.status_code == 200
    obj = response.json()
    assert obj == {'id': 3, 'name': 'Old', 'surname': 'Man', 'age': 86}

def test_get_userlist():
    response = client.get("/api/users/")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{'id': 1, 'name': 'Bob', 'surname': 'Johnson', 'age': 27},
                   {'id': 2, 'name': 'John', 'surname': 'Bobson', 'age': 45},
                   {'id': 3, 'name': 'Old', 'surname': 'Man', 'age': 86}]
    
def test_get_filtered_userlist():
    response = client.get("/api/users/?min_age=30&max_age=50")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{'id': 2, 'name': 'John', 'surname': 'Bobson', 'age': 45}]

# picnic tests

def test_get_empty():
    response = client.get("/api/picnics/")
    assert response.status_code == 200
    obj = response.json()
    assert obj == []

def test_create_picnic_error():
    response = client.post("/api/picnics/")
    assert response.status_code == 422

def test_create_picnic1():
    response = client.post("/api/picnics/?city_id=1&time=2023-10-14T09:52:10.594Z")
    assert response.status_code == 200
    obj = response.json()
    assert obj == {
        "id": 1,
        "city": "Tyumen",
        "time": "2023-10-14T09:52:10.594000+00:00"
    }

def test_create_nofield1_picnic2():
    response = client.post("/api/picnics/?time=2023-11-14T09:52:10.594Z")
    assert response.status_code == 422

def test_create_nofield2_picnic2():
    response = client.post("/api/picnics/?city_id=2")
    assert response.status_code == 422

def test_get_without_users1():
    response = client.get("/api/picnics/?past=true")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{
        "id": 1,
        "city": "Tyumen",
        "users": [],
        "time": "2023-10-14T09:52:10.594000"
    }]

def test_create_picnic2():
    response = client.post("/api/picnics/?time=2123-11-14T09:52:10.594Z&city_id=2")
    assert response.status_code == 200
    obj = response.json()
    assert obj == {
        "id": 2,
        "city": "Helsinki",
        "time": "2123-11-14T09:52:10.594000+00:00"
    }

# modification alters order
def test_get_without_users_both():
    response = client.get("/api/picnics/?past=true")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{
        "id": 2,
        "city": "Helsinki",
        "users": [],
        "time": "2123-11-14T09:52:10.594000"
    },
    {
        "id": 1,
        "city": "Tyumen",
        "users": [],
        "time": "2023-10-14T09:52:10.594000"
    }]

def test_get_without_users2():
    response = client.get("/api/picnics/")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{
        "id": 2,
        "city": "Helsinki",
        "users": [],
        "time": "2123-11-14T09:52:10.594000"
    }]

def test_register1_picnic1():
    response = client.post("/api/picnics/1/register?user_id=1")
    assert response.status_code == 200
    obj = response.json()
    assert obj == {
        "id": 1,
        "city": "Tyumen",
        "time": "2023-10-14T09:52:10.594000",
        "name": "Bob"
    }

def test_register2_picnic1():
    response = client.post("/api/picnics/1/register?user_id=2")
    assert response.status_code == 200
    obj = response.json()
    assert obj == {
        "id": 1,
        "city": "Tyumen",
        "time": "2023-10-14T09:52:10.594000",
        "name": "John"
    }

def test_get_both():
    response = client.get("/api/picnics/?past=true")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{
        "id": 1,
        "city": "Tyumen",
        "users": [{
            "id": 1,
            "name": "Bob",
            "surname": "Johnson",
            "age": 27
        },
        {
            "id": 2,
            "name": "John",
            "surname": "Bobson",
            "age": 45
        }],
        "time": "2023-10-14T09:52:10.594000"
    },
    {
        "id": 2,
        "city": "Helsinki",
        "users": [],
        "time": "2123-11-14T09:52:10.594000"
    }]

def test_get_by_time():
    response = client.get("/api/picnics/?time=2123-11-14T09:52:10.594Z")
    assert response.status_code == 200
    obj = response.json()
    assert obj == [{
        "id": 2,
        "city": "Helsinki",
        "users": [],
        "time": "2123-11-14T09:52:10.594000"
    }]