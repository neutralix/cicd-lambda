import unittest
import json
import os
from triangle_area.lambda_function import lambda_handler

class TestTriangleArea(unittest.TestCase):

    def setUp(self):
        # Backup and clear the COLOUR environment variable before each test
        self.original_colour = os.getenv('COLOUR')
        if 'COLOUR' in os.environ:
            del os.environ['COLOUR']

    def tearDown(self):
        # Restore the original COLOUR environment variable after each test
        if self.original_colour is not None:
            os.environ['COLOUR'] = self.original_colour
        elif 'COLOUR' in os.environ:
            del os.environ['COLOUR']

    def test_valid_input_default_colour(self):
        event = {'base': 10, 'height': 5}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['area'], 25)
        self.assertEqual(body['colour'], 'WHITE')

    def test_valid_input_custom_colour(self):
        os.environ['COLOUR'] = 'RED'
        event = {'base': 10, 'height': 5}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['area'], 25)
        self.assertEqual(body['colour'], 'RED')

    def test_zero_input(self):
        event = {'base': 0, 'height': 5}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 400)

    def test_negative_input(self):
        event = {'base': -10, 'height': 5}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 400)

    def test_missing_input(self):
        event = {}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()
