import json
import unittest

from app import app, db

class ApiSaveTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client
        self.db = db.get_app()

    def test_apiKeySave(self):
        # Given
        payload = json.dumps({
            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
            "deviceType": "desktop"
        })

        header = {
            "Content-Type": "application/json",
        }
        # When
        response = self.app.post('/generateToken', headers=header, data=payload)
        auth_token = response.json['authToken']

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
                     }
        # When
        data = {
                "apiKey": "110t4oh34inkjn4x73c",
                "master": f"{auth_token}",
        }
        response = self.app.post('/apiKey', headers=headers, data=data)
        print(response.json)

        # Then
        self.assertEqual(str, type(response.json['message']))
        self.assertEqual(200, response.status_code)

        def tearDown(self):
            # Delete Database collections after the test is complete
            for collection in self.db.list_collection_names():
                self.db.drop_collection(collection)
