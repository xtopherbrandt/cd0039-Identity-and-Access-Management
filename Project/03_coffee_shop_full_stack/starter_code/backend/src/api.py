import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import requires_auth
from .app import app
from .errors_handling import AuthError

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''


# ROUTES

@app.route('/database', methods=['DELETE'])
@requires_auth('delete:drinks')
def drop_db(jwt):
    success = False
    
    try:
        with app.app_context():
            db_drop_and_create_all()
            success = True
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        abort(500)
            
    return jsonify({
        'success': success
    })

'''
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
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        abort(500)
        
    drinks = [drink.short() for drink in drinks_unformatted]
    success = True
    
    return jsonify({
        'success': success,
        'drinks': drinks
    })

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    success = False
    drinks = []

    try:
        drinks_unformatted = Drink.query.all()
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        abort(500)
        
    drinks = [drink.long() for drink in drinks_unformatted]
    success = True    
    
    return jsonify({
        'success': success,
        'drinks': drinks
    })
    

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    success = False
    
    data = request.get_json()

    if 'title' not in data or 'recipe' not in data:
        print(f'Body must include a title and recipe. {data}')
        abort(400)
    
    drink_with_title = Drink.query.filter_by(title=data['title']).all()
    if len(drink_with_title) > 0:
        print(f'Drink with title {data["title"]} exists')
        abort(400)
        
    recipe = json.dumps(data['recipe'])
    try:
        new_drink = Drink(title=data['title'], recipe=recipe)
        new_drink.insert()
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        abort(500)
       
    return jsonify({
        'success': success,
        'drinks': new_drink.long()
    })

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

