import json
import unittest

from app import app


class ApiDeleteTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_apiKeyDelete_when_Bearer_token_is_correct_then_api_key_delete(self):
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
        data = json.dumps({
                "apiKey": "110t4oh34inkjn4x73c",
                "master": f"{auth_token}",
        })
        response = self.app.delete('/apiKey', headers=headers, data=data)
        self.assertEqual(str, type(response.json['message']))
        self.assertEqual(200, response.status_code)

        self.app.post('/apiKey', headers=headers, data=data)

    def test_apiKeyDelete__when_master_token_expired__then_signature_has_expired(self):
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
        response = self.app.delete('/apiKey', headers=headers, data=data)
        self.assertEqual(403, response.status_code)
        self.assertIsNotNone(response.json['message'])

    def test_apiKeyDelete_when_Bearer_token_is_incorrect__then_Not_enough_segment(self):
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
            "Authorization": f"Bearer blabla"
                     }
        # When
        data = json.dumps({
                "apiKey": "110t4oh34inkjn4x73c",
                "master": f"{auth_token}",
        })
        response = self.app.delete('/apiKey', headers=headers, data=data)
        print(response.json['msg'])

        # Then
        self.assertEqual(422, response.status_code)
        self.assertEqual('Not enough segments', response.json['msg'])
