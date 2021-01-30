import json
import unittest

from app import app


class RefreshTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_refreshToken__when_Bearer_refresh_token_correct__then_auth_token(self):
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
        refresh_token = response.json['refreshToken']

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {refresh_token}"
                     }
        # then
        response = self.app.post('/refreshToken', headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json['authToken'])

    def test_refreshToken__when_auth_token_passed__then_only_refresh_token_allowed(self):
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
            "Authorization": f"Bearer {auth_token}"
                     }
        # then
        response = self.app.post('/refreshToken', headers=headers)
        print("Error:", response.json['msg'])
        self.assertEqual(422, response.status_code)
        self.assertEqual('Only refresh tokens are allowed', response.json['msg'])

    def test_refreshToken__when_Bearer_refresh_token_is_none__then__Missing_Header(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": ""
        }
        # then
        response = self.app.post('/refreshToken', headers=headers)
        print("Error:", response.json['msg'])
        self.assertEqual(401, response.status_code)
        self.assertEqual('Missing Authorization Header', response.json['msg'])

    def test_refreshToken__when_Bearer_refresh_token_is_incorrect__then__not_enough_segments(self):
        # Given
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 'blabla'"
        }
        # then
        response = self.app.post('/refreshToken', headers=headers)
        print("Error:", response.json['msg'])
        self.assertEqual(422, response.status_code)
        self.assertEqual('Not enough segments', response.json['msg'])


