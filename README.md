# people_api
Noyo Code Challenge

# Requirements
- Docker Running
- Docker Compose

# To start the application
`docker-compose up --build` from the top-level directory.

`http://localhost:8080` should be serving the API if it built correctly

# Testing
Make sure you have pytest installed and the API is running,
then run (from the top-level directory):

`python3 -m pytest tests/unit.py`

# Docs

- Create a new person
    - `POST /people/add`
``` 
json params: {
    first_name: required,
    middle_name: optional,
    last_name: required,
    email: required,
    age: required
}
```
- Fetch the latest version of a single person using their id
    - `GET /people/<int:ID>`
- Fetch a single person using their id and a specified version
    - `GET /people/<int:ID>?version=<int:Version>`
- Fetch a list of all persons (latest version)
    - `GET /people`
- Update a single person using their id
    - `PATCH /people/<int:ID>`
    - Params can include any of those from `/people/add`, except here they are opional.
    - This will increment the version number for the person
- Delete a single person using their id
    - `DELETE /people/<int:ID>`
    - This sets a private flag, `deleted: True` in a new version of the PersonVersion object
    - Deleted objects will not be returned when queried, unless a previous version is requested