import json
import unittest

from app import app


class GenerateTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_generateToken__when_master_token_correct__then_correct_auth_refresh_token(self):
        # Given
        payload = json.dumps({
                            "master": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJtWCIsImlhdCI6MTU5MzYzMzczNCwiZXhwIjoyMzI4MDMzNzM0fQ.X45l_iR0nqlHTczwVmP50JO7EEGTAXBwLs_uGLIpbbw",
                            "deviceType": "desktop"
                            })

        headers = {
            "Content-Type": "application/json",
                     }
        # then
        response = self.app.post('/generateToken', headers=headers, data=payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json['authToken'])
        self.assertIsNotNone(response.json['refreshToken'])

    def test_generateToken__when_master_token_None__then_token_is_missing(self):
        # Given
        payload = json.dumps({
                            "master": "",
                            "deviceType": "desktop"
                            })

        headers = {
            "Content-Type": "application/json",
                     }
        # When
        response = self.app.post('/generateToken', headers=headers, data=payload)
        print("Error:", response.json['message'])
        self.assertEqual(403, response.status_code)
        self.assertEqual("Token is missing", response.json['message'])

    def test_generateToken__when_master_token_incorrect__then_token_is_invalid(self):
        # Given
        payload = json.dumps({
                            "master": "blabla",
                            "deviceType": "desktop"
                            })

        headers = {
            "Content-Type": "application/json",
                     }
        # When
        response = self.app.post('/generateToken', headers=headers, data=payload)
        print("Error:", response.json['message'])
        self.assertEqual(403, response.status_code)
        self.assertEqual("Token is invalid", response.json['message'])





