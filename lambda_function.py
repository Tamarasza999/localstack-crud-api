import json
import os
import boto3
import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        print("Event:", json.dumps(event))
        
        path = event.get('path', '')
        http_method = event.get('httpMethod', '')
        
        # GET /users - Get all users
        if path == '/users' and http_method == 'GET':
            return get_all_users()
        
        # GET /users/{id} - Get specific user
        elif '/users/' in path and http_method == 'GET':
            user_id = path.split('/')[-1]
            return get_user(user_id)
        
        # POST /users - Create new user
        elif path == '/users' and http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            return create_user(body)
        
        # PUT /users/{id} - Update user
        elif '/users/' in path and http_method == 'PUT':
            user_id = path.split('/')[-1]
            body = json.loads(event.get('body', '{}'))
            return update_user(user_id, body)
        
        # DELETE /users/{id} - Delete user
        elif '/users/' in path and http_method == 'DELETE':
            user_id = path.split('/')[-1]
            return delete_user(user_id)
        
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

def get_all_users():
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps({'users': response.get('Items', [])})
    }

def get_user(user_id):
    response = table.get_item(Key={'userId': user_id})
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps({'user': response['Item']})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }

def create_user(body):
    user_id = body.get('userId')
    name = body.get('name')
    email = body.get('email')
    
    if not user_id or not name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'userId and name are required'})
        }
    
    table.put_item(Item={
        'userId': user_id,
        'name': name,
        'email': email
    })
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User created successfully'})
    }

def update_user(user_id, body):
    # Check if user exists
    response = table.get_item(Key={'userId': user_id})
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    
    update_expression = "SET"
    expression_attribute_values = {}
    
    if 'name' in body:
        update_expression += " #n = :name,"
        expression_attribute_values[':name'] = body['name']
    
    if 'email' in body:
        update_expression += " email = :email,"
        expression_attribute_values[':email'] = body['email']
    
    # Remove trailing comma
    update_expression = update_expression.rstrip(',')
    
    table.update_item(
        Key={'userId': user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames={'#n': 'name'} if 'name' in body else {}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User updated successfully'})
    }

def delete_user(user_id):
    # Check if user exists
    response = table.get_item(Key={'userId': user_id})
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    
    table.delete_item(Key={'userId': user_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User deleted successfully'})
    }