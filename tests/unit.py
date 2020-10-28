import json
import requests

# TODO: Add negative tests and error handling tests


class TestAPI:
    base_url = "http://localhost:8080"

    person_id = None

    def test_add_update_delete_person(self):
        # Add a person
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
        # Save the person ID
        person_id = text['person_id']

        # Now update the person
        resp = requests.patch(
            f"{self.base_url}/people/update/{person_id}",
            json={
                "middle_name": "'Cherry'"
            }
        )
        assert resp.status_code == 200
        payload = json.loads(resp.text)
        assert payload["middle_name"] == "'Cherry'"
        assert payload['version'] == 2

        # Get the previous version
        resp = requests.get(
            f"{self.base_url}/people/{person_id}?version=1"
        )
        payload = json.loads(resp.text)
        assert payload['first_name'] == 'Jerry'
        assert payload['middle_name'] is None
        assert payload['version'] == 1

        # Now delete the person
        resp = requests.delete(
            f"{self.base_url}/people/delete/{person_id}"
        )

        assert resp.status_code == 200
        assert json.loads(resp.text)['deleted'] is True

        # Now try to get the deleted person
        resp = requests.get(
            f"{self.base_url}/people/{person_id}"
        )
        assert resp.status_code == 404

    def test_get_people(self):
        resp = requests.post(
            f"{self.base_url}/people/add",
            json={
                "first_name": "Bob",
                "last_name": "Weir",
                "email": "shorts@dead.com",
                "age": 53
            }
        )
        assert resp.status_code == 200
        resp = requests.get(
            f"{self.base_url}/people"
        )
        assert resp.status_code == 200
        assert len(json.loads(resp.text)) > 1
