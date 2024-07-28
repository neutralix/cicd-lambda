import unittest
import json
from triangle_area.lambda_function import lambda_handler

class TestTriangleArea(unittest.TestCase):

    def test_valid_input(self):
        event = {'base': 10, 'height': 5}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body'])['area'], 25)

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
