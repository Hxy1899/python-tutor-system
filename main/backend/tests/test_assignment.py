def test_create_assignment(client):
    response = client.post(
        "/api/v1/assignments/",
        json={
            "title": "Test Assignment",
            "description": "Test Description",
            "test_code": "def test_it(): pass"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Assignment"
    assert "id" in data

def test_get_assignments(client):
    # Create one first
    client.post(
        "/api/v1/assignments/",
        json={"title": "A1", "description": "D1", "test_code": ""},
    )
    
    response = client.get("/api/v1/assignments/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(a["title"] == "A1" for a in data)

def test_get_assignment(client):
    res = client.post(
        "/api/v1/assignments/",
        json={"title": "A2", "description": "D2", "test_code": ""},
    )
    assignment_id = res.json()["id"]
    
    response = client.get(f"/api/v1/assignments/{assignment_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "A2"
