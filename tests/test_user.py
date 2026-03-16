
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