
def test_create_user(client):
    user_data = {
        "full_name": "Rakesh",
        "email": "Rakesh@gmail.com",
        "password": "password123",
        "role": "free"
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201


def test_get_user(authorized_access, test_user):
    user_id = test_user['id']
    response = authorized_access.get(f"/users/{user_id}")
    assert response.status_code == 200


def test_update_user(authorized_access, test_user):
    updated_data = {
        "full_name": "Rakesh Kumar"
    }
    response = authorized_access.patch(
        f"/users/{test_user['id']}",
        json=updated_data
    )
    assert response.status_code == 202
    assert response.json()["full_name"] == "Rakesh Kumar"