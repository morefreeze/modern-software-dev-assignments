def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_patch_nonexistent_action_item(client):
    r = client.patch("/action-items/999", json={"description": "Not Found"})
    assert r.status_code == 404


def test_complete_nonexistent_action_item(client):
    r = client.put("/action-items/999/complete")
    assert r.status_code == 404


def test_list_action_items_invalid_sort(client):
    r = client.get("/action-items/", params={"sort": "invalid_field"})
    assert r.status_code == 200


def test_list_action_items_completed_false(client):
    payload = {"description": "Test Item"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201

    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_patch_action_item_with_empty_payload(client):
    payload = {"description": "Test Description"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item_id = r.json()["id"]

    r = client.patch(f"/action-items/{item_id}", json={})
    assert r.status_code == 200
    assert r.json()["description"] == "Test Description"
    assert r.json()["completed"] is False


def test_patch_action_item_completed_status(client):
    payload = {"description": "Test Description"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item_id = r.json()["id"]

    r = client.patch(f"/action-items/{item_id}", json={"completed": True})
    assert r.status_code == 200
    assert r.json()["completed"] is True


