def test_plans_endpoint_returns_200_list(client):
    res = client.get("/api/plans")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_plans_ids_in_pricing_page_order(client):
    plans = client.get("/api/plans").json()
    assert [p["id"] for p in plans] == ["starter", "team", "enterprise"]


def test_plans_fields_present(client):
    for plan in client.get("/api/plans").json():
        assert "id" in plan
        assert "name" in plan
        assert "price" in plan
