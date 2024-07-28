import unittest
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def test_lambda_handler(self):
        response = lambda_handler({}, {})
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Hello from Lambda!', response['body'])

if __name__ == '__main__':
    unittest.main()
