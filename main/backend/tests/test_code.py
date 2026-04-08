def test_submit_code_correct(client):
    # Setup: Create student and assignment
    res_u = client.post("/api/v1/auth/register", json={"username": "s1", "password": "p1", "name": "S1", "role": "student"})
    user_id = res_u.json()["id"]
    res_a = client.post("/api/v1/assignments/", json={"title": "T1", "description": "D1", "test_code": "def test_solution(): pass"})
    assignment_id = res_a.json()["id"]
    
    # Submit correct code
    response = client.post(
        "/api/v1/code/submit",
        json={
            "user_id": user_id,
            "assignment_id": assignment_id,
            "code": "print('hello')",
            "test_code": ""
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] == True
    assert data["error_type"] == "Correct"

def test_submit_code_syntax_error(client):
    # Setup: Create student and assignment
    res_u = client.post("/api/v1/auth/register", json={"username": "s2", "password": "p2", "name": "S2", "role": "student"})
    user_id = res_u.json()["id"]
    res_a = client.post("/api/v1/assignments/", json={"title": "T2", "description": "D2", "test_code": ""})
    assignment_id = res_a.json()["id"]
    
    # Submit code with syntax error
    response = client.post(
        "/api/v1/code/submit",
        json={
            "user_id": user_id,
            "assignment_id": assignment_id,
            "code": "print('hello' + )", # Syntax error
            "test_code": ""
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] == False
    assert data["error_type"] == "SyntaxError"
    assert "hint" in data
