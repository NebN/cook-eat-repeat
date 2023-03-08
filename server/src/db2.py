import os
import sys
import dataclasses
import uuid
from tinydb import TinyDB
from tinydb.table import Document
from src.model import Ingredient, Recipe, RecipeIngredient, Meal
import logging


db = TinyDB(os.path.join(sys.path[0], 'database.db'))
ingredients = db.table('ingredients')
recipes = db.table('recipes')
meals = db.table('meals')
history = db.table('history')

logger = logging.getLogger()


def ided_dataclass_to_document(dataclass):
  asdict = dataclasses.asdict(dataclass)
  existing_id = asdict.pop('id')
  id = existing_id if existing_id is not None else uuid.uuid4()
  return Document(asdict, doc_id=id)


def all_ingredients():
  return ingredients.all()


def set_favourite(id, favourite):
  pass


def save_ingredient(ingredient):
  ingredients.upsert(ided_dataclass_to_document(ingredient))
    

def delete_ingredient(id):
  pass


def save_recipe(recipe, ingredients):
  if recipe.id is None:
    logger.debug('inserting %s with %s', recipe, ingredients)
    return _insert_recipe(recipe, ingredients)
  else:
    logger.debug('updating %s with %s', recipe, ingredients)
    return _update_recipe(recipe, ingredients)


def save_meal(meal):
  if meal.id is None:
    logger.debug('inserting %s', meal)
    return _insert_meal(meal)
  else:
    logger.debug('updating %s', meal)
    return _update_meal(meal)


def _insert_ingredient(ingredient):
  pass


def _insert_recipe_ingredients(recipe_ingredients):
  pass


def _update_ingredient(ingredient):
  pass
  

def _insert_recipe(recipe, ingredients):
  pass


def _update_recipe(recipe, ingredients):
  pass
  

def _insert_meal(meal):
  pass


def _update_meal(meal):
  pass
  