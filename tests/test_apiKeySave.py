import json
import unittest

from app import app, db


class ApiSaveTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_apiKeySave__when_master_token_and_api_key_given__then_saving_api_key(self):
        # Given
        payload = json.dumps({
            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
            "deviceType": "desktop"
        })

        header = {
            "Content-Type": "application/json",
        }

        response = self.app.post('/generateToken', headers=header, data=payload)
        auth_token = response.json['authToken']
        # When
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
                     }

        data = json.dumps({
                "apiKey": "110t4oh34inkjn4x73c",
                "master": f"{auth_token}",
        })

        # Then
        response = self.app.post('/apiKey', headers=headers, data=data)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json['message'])

        self.app.delete('/apiKey', headers=headers, data=data)

    def test_apiKeySave__when_master_token_expired__then_signature_has_expired(self):
        # Given
        payload = json.dumps({
            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
            "deviceType": "desktop"
        })

        header = {
            "Content-Type": "application/json",
        }

        response = self.app.post('/generateToken', headers=header, data=payload)
        auth_token = response.json['authToken']
        # When
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
                     }

        data = json.dumps({
                "apiKey": "110t4oh34inkjn4x73c",
                "master": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTIxNjMzNzAsIm5iZiI6MTYxMjE2MzM3MCwianRpIjoiMjYzMjEyYjAtMzgxOC00YjUyLWIzZjktNDFiYzQwNTFhOWQzIiwiZXhwIjoxNjEyMTY0MjcwLCJpZGVudGl0eSI6InJtWCIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.2mUtbVJfQOjLI83F_EPV_VOVvFe1gOu8NO_vkhF7Vg4",
        })

        # Then
        response = self.app.post('/apiKey', headers=headers, data=data)
        self.assertEqual(403, response.status_code)
        self.assertIsNotNone(response.json['message'])

    def test_apiKeySave__when_Bearer_token_incorrect__then_saving_api_key(self):
        # Given
        payload = json.dumps({
            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
            "deviceType": "desktop"
        })

        header = {
            "Content-Type": "application/json",
        }

        response = self.app.post('/generateToken', headers=header, data=payload)
        auth_token = response.json['authToken']

        # When
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer blabla"
                     }

        data = json.dumps({
                "apiKey": "110t4oh34inkjn4x73c",
                "master": f"{auth_token}",
        })

        # Then
        response = self.app.post('/apiKey', headers=headers, data=data)
        print('Error:', response.json["msg"])
        self.assertEqual(422, response.status_code)
        self.assertEqual('Not enough segments', response.json["msg"])


