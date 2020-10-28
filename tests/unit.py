import json
import requests


class TestAPI:
    base_url = "http://localhost:8080"

    person_id = None

    def test_add_and_update_person(self):
        resp = requests.post(
            f"{self.base_url}/people/add",
            json={
                "first_name": "Jerry",
                "last_name": "Garcia",
                "email": "head@dead.com",
                "age": 53
            }
        )
        assert resp.status_code == 200
        text = json.loads(
            resp.text
        )
        person_id = text['person_id']

        # Now update the perspon
        print("\n\nPerson ID: ", person_id)
        resp = requests.patch(
            f"{self.base_url}/people/update/{person_id}",
            json={
                "middle_name": "'Cherry'"
            }
        )
        assert resp.status_code == 200
        print(resp.text)

    def test_get_people(self):
        resp = requests.get(
            f"{self.base_url}/people"
        )
        assert resp.status_code == 200
