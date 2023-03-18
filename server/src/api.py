import traceback
from functools import wraps
from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
import dataclasses
import logging
from src import db as db
from src.model import Ingredient, Amount, Meal, Goal
from src import util

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ['http://localhost:8080', 'http://192.168.1.*:.*']}})

logger = logging.getLogger()


def error_managed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as error:
            logger.error('Unhandled exception during %s: %s', f.__name__, error)
            logger.debug(traceback.format_exc())
            return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    return wrapper


@app.route('/api/ingredient', methods=['GET', 'POST', 'DELETE'])
@error_managed
def ingredient():
    if request.method == 'GET':
        return all_ingredients()
    elif request.method == 'POST':
        return save_ingredient()
    elif request.method == 'DELETE':
        return delete_ingredient()


@app.route('/api/meal', methods=['GET', 'POST', 'DELETE'])
@error_managed
def meal():
    if request.method == 'GET':
        return all_meals()
    elif request.method == 'POST':
        return save_meal()
    elif request.method == 'DELETE':
        return delete_meal()


@app.route('/api/meal/history', methods=['GET'])
@error_managed
def meal_history():
    meals = db.all_cooked_meals()
    return meals, HTTPStatus.OK


@app.route('/api/meal/eat', methods=['POST'])
@error_managed
def eat_meal():
    data = request.get_json()
    id = data['id']
    date = util.string_to_date(data['date'])
    logger.debug('Eating meal id %s on day %s', id, date)
    update = db.eat_meal(id, date)
    return update, HTTPStatus.OK


@app.route('/api/goal', methods=['POST', 'GET'])
@error_managed
def goal():
    if request.method == 'POST':
        return save_goal()
    elif request.method == 'GET':
        return current_goal()


@app.route('/api/goal/today', methods=['GET'])
@error_managed
def todays_progress():
    progress = db.todays_progress()
    return progress, HTTPStatus.OK


@app.route('/api/goal/all', methods=['GET'])
@error_managed
def all_progress():
    progress = db.all_progress()
    return progress, HTTPStatus.OK


@app.route('/api/ingredient/favourite', methods=['POST'])
@error_managed
def set_favourite_ingredient():
    data = request.get_json()
    id = data['id']
    logger.debug('Toggling favourite ingredient for id=%s', id)
    res = db.toggle_favourite_ingredient(id=id)
    return {'newFavourite': res}, HTTPStatus.OK


@app.route('/api/meal/favourite', methods=['POST'])
@error_managed
def set_favourite_meal():
    data = request.get_json()
    id = data['id']
    logger.debug('Toggling favourite meal for id=%s', id)
    res = db.toggle_favourite_meal(id=id)
    return {'newFavourite': res}, HTTPStatus.OK     

def save_goal():
    data = request.get_json()
    calories = data['calories']
    protein = data['protein']
    goal = Goal(calories, protein)
    logger.debug('Saving goal %s', goal)
    db.save_goal(goal)
    return {'from_day': goal.from_day}, HTTPStatus.OK


def current_goal():
    goal = db.current_goal()
    return dataclasses.asdict(goal), HTTPStatus.OK


def all_meals():
    return db.all_meals()


def all_ingredients():
    return db.all_ingredients()


def save_ingredient():
    data = request.get_json()
    label = data['label']
    calories = data['calories']
    protein = data['protein']
    serving_size = data['serving_size']

    ingredient = Ingredient(label=label, calories=calories, protein=protein, serving_size=serving_size)

    logger.debug('Adding new ingredient %s', ingredient)
    db.save_ingredient(ingredient)
    return dataclasses.asdict(ingredient), HTTPStatus.OK


def delete_ingredient():
    data = request.get_json()
    id = data['id']
    logger.debug('Deleting ingredient id %s', id)
    id = db.delete_ingredient(id)
    return {}, HTTPStatus.OK


def save_meal():
    data = request.get_json()
    label = data['label']
    calories = data['calories']
    protein = data['protein']
    meals_remaining = data['meals_remaining']
    ingredients = [(
        Ingredient(
            label=i['label'],
            calories=i['calories'],
            protein=i['protein'],
            serving_size=i['serving_size']), 
        Amount(
            grams=i['grams'], 
            servings=i['servings'],
            per_meal=i['per_meal'])) for i in data['ingredients']
    ]


    meal = Meal(label, ingredients, calories=calories, protein=protein, meals_remaining=meals_remaining)

    logger.debug('Adding new meal %s', meal)
    db.save_meal(meal)
    return dataclasses.asdict(meal), HTTPStatus.OK


def delete_meal():
    data = request.get_json()
    id = data['id']
    logger.debug('Deleting meal id %s', id)
    db.delete_meal(id)
    return {}, HTTPStatus.OK