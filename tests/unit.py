import requests


class TestAPI:
    base_url = "http://localhost:8080"

    def test_add_person(self):
        resp = requests.post(
            f"{self.base_url}/people/add",
            json={
                "first_name": "Jerry"
            }
        )
        print(resp)
        assert resp.status_code == 200

    def test_get_people(self):
        resp = requests.get(
            f"{self.base_url}/people"
        )
        assert resp.status_code == 200
