
def test_create_rate_limit(authorized_access):
    request_data = {
        "role":"admin",
        "requests_limit":50,
        "time_window":5
    }
    response = authorized_access.post('/rate_limit_rules/',json=request_data)

    assert response.status_code == 201

def test_get_rate_limits(authorized_access):
    response = authorized_access.get('/rate_limit_rules/')
    assert response.status_code == 200

def test_get_rate_limit(authorized_access,create_rate_limit_rule):
    limit_id = create_rate_limit_rule['id']

    response = authorized_access.get(f'/rate_limit_rules/{limit_id}/')
    
    assert response.json()['role'] == "admin"
    assert response.status_code == 200

def test_update_rate_limit(authorized_access,create_rate_limit_rule):
    limit_id = create_rate_limit_rule['id']

    request_data = {
        "role":"admin",
        "requests_limit":550,
        "time_window":50
    }

    response = authorized_access.put(
        f'/rate_limit_rules/{limit_id}/',
        json=request_data
    )

    assert response.json()['requests_limit'] == 550
    assert response.status_code == 202


def test_delete_rule_limit(authorized_access,create_rate_limit_rule):
    limit_id = create_rate_limit_rule['id']
    response = authorized_access.delete(f'/rate_limit_rules/{limit_id}/')
    assert response.status_code == 204