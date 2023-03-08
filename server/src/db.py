import os
import sys
import sqlite3 as sl
import dataclasses
from src.model import Ingredient, Recipe, RecipeIngredient, Meal
import logging


con = sl.connect(os.path.join(sys.path[0], 'test.db'), check_same_thread=False)
logger = logging.getLogger()

sql_location = os.path.join(sys.path[0], *['res', 'create_tables.sql'])
with open(sql_location, 'r') as sql_file:
  sql = sql_file.read()
  with con:
    con.cursor().executescript(sql)

def all_ingredients():
  with con:
    res = con.cursor().execute('SELECT * FROM ingredient ORDER BY favourite DESC, label ASC')
    return [Ingredient(*r) for r in res.fetchall()]


def set_favourite(id, favourite):
  with con:
    res = con.cursor().execute('''
    UPDATE ingredient 
    SET favourite = ? 
    WHERE id = ?
    RETURNING favourite''', [favourite, id])
    return res.fetchone()[0] == 1



def save_ingredient(ingredient):
  if ingredient.id is None:
    logger.debug('inserting %s', ingredient)
    return _insert_ingredient(ingredient)
  else:
    logger.debug('updating %s', ingredient)
    return _update_ingredient(ingredient)
    

def delete_ingredient(id):
    with con:
      con.cursor().execute('''
      DELETE 
      FROM ingredient 
      WHERE id = ?''', [id])


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
  with con:
    res = con.cursor().execute('''
    INSERT INTO ingredient (label, calories, proteins, serving_size) 
    VALUES(?,?,?,?)
    RETURNING id''', 
    [ingredient.label, ingredient.calories, ingredient.proteins, ingredient.serving_size])
    
    return res.fetchone()[0]


def _insert_recipe_ingredients(recipe_ingredients):
  with con:
    con.cursor().executemany('''
    INSERT INTO recipe_ingredient(recipe_id, ingredient_id, amount_grams, amount_servings)
    VALUES(?,?,?,?)''',
    [(i.recipe_id, i.ingredient_id, i.amount_grams, i.amount_servings) for i in recipe_ingredients])


def _update_ingredient(ingredient):
  with con:
    con.cursor().execute('''
    UPDATE ingredient
    SET label=?,
    calories=?,
    proteins=?,
    serving_size=?
    WHERE id=?''', 
    [ingredient.label, ingredient.calories, ingredient.proteins, ingredient.serving_size, ingredient.id])

    return ingredient.id 
  

def _insert_recipe(recipe, ingredients):
  with con:
    cursor = con.cursor()
    res = cursor.execute('''
    INSERT INTO recipe (label) 
    VALUES(?)
    RETURNING id''', 
    [recipe.label])
    
    recipe_id = res.fetchone()[0]
    ingredients_with_id = [dataclasses.replace(i, recipe_id=recipe_id) for i in ingredients]

    _insert_recipe_ingredients(ingredients_with_id)

    return recipe_id


def _update_recipe(recipe, ingredients):
  pass
  

def _insert_meal(meal):
  with con:
    res = con.cursor().execute('''
    INSERT INTO meal (recipe_id, calories, protein, meals_created, meals_remaining) 
    VALUES(?,?,?,?,?)
    RETURNING id''', 
    [meal.recipe_id, meal.calories, meal.protein, meal.meals_created, meal.meals_remaining])
    return res.fetchone()[0]
    

def _update_meal(meal):
  pass
  