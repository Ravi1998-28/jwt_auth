import json
import unittest

from app import app


class ProtectedTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_protected__when__auth_token_or_api_key_passed__then_user_name(self):
        # Given
        payload = json.dumps({
            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
            "deviceType": "desktop"
        })

        headers = {
            "Content-Type": "application/json",
        }
        # When
        response = self.app.post('/generateToken', headers=headers, data=payload)
        auth_token = response.json['authToken']

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{auth_token}",
            "x-api-key": "110t4oh34inkjn4x73c"
        }

        response = self.app.post('/protected', headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json['logged_in_as'])

    def test_protected__when__user_not_in_table__then_user_not_exist(self):
        # Given
        payload = json.dumps({
            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
            "deviceType": "desktop"
        })

        headers = {
            "Content-Type": "application/json",
        }
        # When
        response = self.app.post('/generateToken', headers=headers, data=payload)
        auth_token = response.json['authToken']

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{auth_token}",
            "x-api-key": "110t4oh34inkjn4x73c"
        }

        response = self.app.post('/protected', headers=headers)
        print("Error:", response.json['message'])
        self.assertEqual(403, response.status_code)
        self.assertEqual('user does not exist', response.json['message'])

    def test_protected__when__token_and_api_key_missing__then_Authorisation_token_missing(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "",
            "x-api-key": ""
        }

        response = self.app.post('/protected', headers=headers)
        print("Error:", response.json['message'])
        self.assertEqual(401, response.status_code)
        self.assertEqual('Authorisation header is missing', response.json['message'])
