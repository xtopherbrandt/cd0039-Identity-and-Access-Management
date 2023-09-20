import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
with app.app_context():
    setup_db(app)

CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#with app.app_context():
#    db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    success = False
    drinks = []
    try:
        drinks_unformatted = Drink.query.all()
    except:
        abort(500)
        
    drinks = [drink.short() for drink in drinks_unformatted]
    success = True
    
    return jsonify({
        'success': success,
        'drinks': drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    
@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400, 
        "message": "bad request"
    }), 400
    
@app.errorhandler(401)
def handle_unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401, 
        "message": "unauthorized"
    }), 401
    
@app.errorhandler(403)
def handle_forbidden(error):
    return jsonify({
        "success": False, 
        "error": 401, 
        "message": "forbidden"
    }), 403
        
@app.errorhandler(404)
def handle_resource_not_found(self):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found.'
    }), 404
    
@app.errorhandler(405)
def handle_method_not_allowed(self):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed.'
    }), 405
    
    
@app.errorhandler(422)
def handle_unprocessable_content(self):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Content.'
    }), 422        

@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500, 
        "message": "Server error."
    }), 500