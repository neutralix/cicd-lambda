import json
import os

def lambda_handler(event, context):
    colour = os.getenv('COLOUR', 'WHITE')
    try:
        base = float(event.get('base', 0))
        height = float(event.get('height', 0))
        if base <= 0 or height <= 0:
            raise ValueError("Base and height must be positive numbers.")

        area = 0.5 * base * height
        return {
            'statusCode': 200,
            'body': json.dumps({'area': area, 'colour': colour})
        }
    except (TypeError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
