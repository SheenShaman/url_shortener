from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_shorten():
    result = client.post(
        url="/shorten",
        json={"url": "https://www.google.com"}
    )
    short_url = result.json()["short_url"]

    assert result.status_code == 200
    assert short_url[:-6] == 'http://localhost:8000/'


def test_redirect():
    result = client.post(
        "/shorten",
        json={"url": "https://example.com"}
    )
    short_url = result.json()["short_url"]
    code = short_url.split("/")[-1]
    response = client.get(f"/{code}", follow_redirects=False)

    assert response.status_code in [302, 307]


def test_stats():
    result = client.post(
        "/shorten",
        json={"url": "https://example.com"}
    )
    short_url = result.json()["short_url"]
    code = short_url.split("/")[-1]
    client.get(f"/{code}")
    client.get(f"/{code}")
    stats = client.get(f"/stats/{code}")

    assert stats.status_code == 200
    assert stats.json()["clicks"] == 2
