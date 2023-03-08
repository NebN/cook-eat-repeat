from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
import dataclasses
import sqlite3
import logging
from src import db2 as db
from src.model import Ingredient, Recipe, RecipeIngredient, Meal

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ['http://localhost:8080', 'http://192.168.1.*:.*']}})

logger = logging.getLogger()

@app.route('/api/ingredient', methods=['GET', 'POST'])
def save_ingredient():
    if request.method == 'GET':
        logger.debug('Getting all ingredients')
        return db.all_ingredients()
    else:
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

        except sqlite3.IntegrityError as error:
            logger.error('IntegrityError during save_ingredient: %s', error)
            return {'errorMessage': f'{ingredient.label} already exists'}, HTTPStatus.NOT_ACCEPTABLE
            
        except sqlite3.Error as error:
            logger.error('Error during save_ingredient: %s', error)
            return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR

        except Exception as error:
            logger.error('Unhandled exception during save_ingredient: %s', error)
            return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR



@app.route('/api/ingredient', methods=['DELETE'])
def delete_ingredient():
    data = request.get_json()
    id = data['id']
    logger.debug('Deleting ingredient id %s', id)
    try:
        id = db.delete_ingredient(id)
        return {}, HTTPStatus.OK

    except sqlite3.Error as error:
        logger.error('Error during delete_ingredient: %s', error)
        return {}, HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as error:
        logger.error('Unhandled exception during delete_ingredient: %s', error)
        return {}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/api/ingredient/favourite', methods=['POST'])
def set_favourite():
    data = request.get_json()
    id = data['id']
    oldFavourite = data['oldFavourite']
    newFavourite = data['newFavourite']
    logger.debug('Setting favourite=%s for id=%s', newFavourite, id)
    try:
        res = db.set_favourite(id=id, favourite=newFavourite)
        return {'newFavourite': res}, HTTPStatus.OK
    except sqlite3.Error as error:
        logger.error('Error during set_favourite: %s', error)
        return {'newFavourite': oldFavourite}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as error:
        logger.error('Unhandled exception during set_favourite: %s', error)
        return {}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/api/recipe', methods=['POST'])
def save_recipe():
    data = request.get_json()
    # id = data.get('id', None)
    recipe = Recipe(id=None, label=data['label'], ingredient_ids=[])
    ingredients = [RecipeIngredient(None, i.id, i.amount_grams, i.amount_servings) for i in  data['ingredients']]
    db.save_recipe(recipe, ingredients)

    logger.debug('Adding new recipe %s with %s', recipe, ingredients)
    try:
        db.save_recipe(recipe, ingredients)
        return {}, HTTPStatus.OK

    except sqlite3.IntegrityError as error:
        logger.error('IntegrityError during save_recipe: %s', error)
        return {'errorMessage': f'{recipe.label} already exists'}, HTTPStatus.NOT_ACCEPTABLE
        
    except sqlite3.Error as error:
        logger.error('Error during save_recipe: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as error:
        logger.error('Unhandled exception during save_recipe: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR



@app.route('/api/meal', methods=['POST'])
def save_meal():
    data = request.get_json()
    recipe_id = data.get('recipe_id', None)

    if recipe_id is None:
        recipe = Recipe(id=None, label=data['label'], ingredient_ids=[])
        ingredients = [RecipeIngredient(None, i['id'], i['amount_grams'], i['amount_servings']) for i in  data['ingredients']]
        recipe_id = db.save_recipe(recipe, ingredients)

    calories = data['calories']
    protein = data['protein']
    meals_created = data['meals_created']
    meal = Meal(None, recipe_id, calories, protein, meals_created, meals_remaining=meals_created)

    logger.debug('Adding new meal %s', meal)
    try:
        db.save_meal(meal)
        return {}, HTTPStatus.OK

    except sqlite3.IntegrityError as error:
        logger.error('IntegrityError during save_meal: %s', error)
        return {'errorMessage': f'{recipe.label} already exists'}, HTTPStatus.NOT_ACCEPTABLE
        
    except sqlite3.Error as error:
        logger.error('Error during save_meal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as error:
        logger.error('Unhandled exception during save_meal: %s', error)
        return {'errorMessage': 'unexpected error'}, HTTPStatus.INTERNAL_SERVER_ERROR