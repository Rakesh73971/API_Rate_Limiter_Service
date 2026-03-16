def test_create_request_log(authorized_access):

    request_data = {
        "endpoint": "/users",
        "status_code": 200,
        "method":'GET'
    }

    response = authorized_access.post(
        "/request_logs/",
        json=request_data
    )

    assert response.status_code == 201
    assert response.json()["endpoint"] == "/users"
    assert response.json()["status_code"] == 200

def test_get_request_logs(authorized_access):
    response = authorized_access.get('/request_logs/')
    assert response.status_code == 200

def test_get_request_log(authorized_access,create_request_log):
    request_id = create_request_log['id']
    response = authorized_access.get(f'/request_logs/{request_id}/')

    assert response.json()['status_code'] == 200
    assert response.status_code == 200


def test_update_request_log(authorized_access,create_request_log):
    request_id = create_request_log['id']
    request_data = {
        'endpoint':'/request_logs',
        'status_code':201,
        'method':'POST'
    }
    response = authorized_access.put(f'/request_logs/{request_id}/',json=request_data)
    assert response.status_code == 202
    assert response.json()['status_code'] == 201

def test_delete_request_log(authorized_access,create_request_log):
    request_id = create_request_log['id']
    response = authorized_access.delete(f'/request_logs/{request_id}/')
    assert response.status_code == 204

