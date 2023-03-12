from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
import dataclasses
import logging
from src import db as db
from src.model import Ingredient, Amount, Meal, Goal

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ['http://localhost:8080', 'http://192.168.1.*:.*']}})

logger = logging.getLogger()

@app.route('/api/ingredient', methods=['GET', 'POST', 'DELETE'])
def ingredient():
    if request.method == 'GET':
        return all_ingredients()
    elif request.method == 'POST':
        return save_ingredient()
    elif request.method == 'DELETE':
        return delete_ingredient()


@app.route('/api/meal', methods=['GET', 'POST', 'DELETE'])
def meal():
    if request.method == 'GET':
        return all_meals()
    elif request.method == 'POST':
        return save_meal()
    elif request.method == 'DELETE':
        return delete_meal()


@app.route('/api/meal/eat', methods=['POST'])
def eat_meal():
    data = request.get_json()
    id = data['id']
    logger.debug('Eating meal id %s', id)
    try:
        update = db.eat_meal(id)
        return update, HTTPStatus.OK
    except Exception as error:
        logger.error('Unhandled exception during eat_meal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/api/goal', methods=['POST', 'GET'])
def goal():
    if request.method == 'POST':
        return save_goal()
    elif request.method == 'GET':
        return current_goal()


@app.route('/api/goal/today', methods=['GET'])
def todays_progress():
    try:
        progress = db.todays_progress()
        return progress, HTTPStatus.OK
    except Exception as error:
        logger.error('Unhandled exception during current_goal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/api/ingredient/favourite', methods=['POST'])
def set_favourite():
    data = request.get_json()
    id = data['id']
    logger.debug('Toggling favourite for id=%s', id)
    try:
        res = db.toggle_favourite(id=id)
        return {'newFavourite': res}, HTTPStatus.OK
    
    except Exception as error:
        logger.error('Unhandled exception during set_favourite: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

def save_goal():
    data = request.get_json()
    calories = data['calories']
    protein = data['protein']
    goal = Goal(calories, protein)
    logger.debug('Saving goal%s', goal)
    try:
        db.save_goal(goal)
        return {'from_day': goal.from_day}, HTTPStatus.OK
    except Exception as error:
        logger.error('Unhandled exception during save_goal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


def current_goal():
    try:
        goal = db.current_goal()
        return dataclasses.asdict(goal), HTTPStatus.OK
    except Exception as error:
        logger.error('Unhandled exception during current_goal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


def all_meals():
    return db.all_meals()


def all_ingredients():
    return db.all_ingredients()


def save_ingredient():
    data = request.get_json()
    id = data.get('id', None)
    label = data['label']
    calories = data['calories']
    proteins = data['proteins']
    serving_size = data['serving_size']

    ingredient = Ingredient(id=id, label=label, calories=calories, proteins=proteins, serving_size=serving_size)

    logger.debug('Adding new ingredient %s', ingredient)
    try:
        id = db.save_ingredient(ingredient)
        return dataclasses.asdict(dataclasses.replace(ingredient, id=id)), HTTPStatus.OK

    except Exception as error:
        logger.error('Unhandled exception during save_ingredient: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


def delete_ingredient():
    data = request.get_json()
    id = data['id']
    logger.debug('Deleting ingredient id %s', id)
    try:
        id = db.delete_ingredient(id)
        return {}, HTTPStatus.OK

    except Exception as error:
        logger.error('Unhandled exception during delete_ingredient: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


def save_meal():
    data = request.get_json()
    label = data['label']
    calories = data['calories']
    protein = data['protein']
    meals_created = data['meals_created']
    logger.info(data)
    ingredients = [(
        Ingredient(
            id=i['id'],
            label=i['label'],
            calories=i['calories'],
            proteins=i['protein'],
            serving_size=i['serving_size']), 
        Amount(
            grams=i['grams'], 
            servings=i['servings'])) for i in data['ingredients']
    ]


    meal = Meal(None, label, ingredients, calories=calories, protein=protein, meals_created=meals_created, meals_remaining=meals_created)

    logger.debug('Adding new meal %s', meal)
    try:
        id = db.save_meal(meal)
        return dataclasses.asdict(dataclasses.replace(meal, id=id)), HTTPStatus.OK

    except Exception as error:
        logger.error('Unhandled exception during save_meal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR


def delete_meal():
    data = request.get_json()
    id = data['id']
    logger.debug('Deleting meal id %s', id)
    try:
        id = db.delete_meal(id)
        return {}, HTTPStatus.OK

    except Exception as error:
        logger.error('Unhandled exception during delete_meal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR