def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    # Test invalid sort field falls back to default sort
    r = client.get("/notes/", params={"sort": "-nonexistent"})
    assert r.status_code == 200

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"

    # Test PATCH with empty payload (no changes)
    r = client.patch(f"/notes/{note_id}", json={})
    assert r.status_code == 200

    # Test GET non-existent note - should return 404
    r = client.get("/notes/999999")
    assert r.status_code == 404

    # Test PATCH non-existent note - should return 404
    r = client.patch("/notes/999999", json={"title": "Should fail"})
    assert r.status_code == 404


def test_get_nonexistent_note(client):
    r = client.get("/notes/999")
    assert r.status_code == 404


def test_patch_nonexistent_note(client):
    r = client.patch("/notes/999", json={"title": "Not Found"})
    assert r.status_code == 404


def test_patch_note_with_empty_payload(client):
    payload = {"title": "Test", "content": "Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={})
    assert r.status_code == 200
    assert r.json()["title"] == "Test"
    assert r.json()["content"] == "Content"


def test_patch_note_content_only(client):
    payload = {"title": "Test", "content": "Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={"content": "Updated Content"})
    assert r.status_code == 200
    assert r.json()["content"] == "Updated Content"


def test_get_existing_note(client):
    payload = {"title": "Test", "content": "Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test"


def test_list_notes_invalid_sort(client):
    r = client.get("/notes/", params={"sort": "invalid_field"})
    assert r.status_code == 200


