import os
import sys
import dataclasses
from datetime import datetime, date
from tinydb import TinyDB, Query
import logging
from src import util
from src.model import Goal, DayProgress

db = TinyDB(os.path.join(sys.path[0], 'database.db'))
ingredients = db.table('ingredients')
meals = db.table('meals')
favourite_meals = db.table('favourite_meals')
goals = db.table('goals')
days_progress = db.table('days_progress')


logger = logging.getLogger()


def document_id_to_id(*items):
  def with_id(item):
    item['id'] = item.doc_id
    return item
  return [with_id(item) for item in items]


def all_ingredients():
  return document_id_to_id(*ingredients.all())


def toggle_favourite(id):
  def toggle(doc):
    doc['favourite'] = not doc['favourite']
    return doc
    
  ingredients.update(toggle, doc_ids=[id])
  return ingredients.get(doc_id=id)['favourite']


def save_ingredient(ingredient):
  res = ingredients.upsert(dataclasses.asdict(ingredient), Query().label == ingredient.label)
  return res[0]
    

def delete_ingredient(id):
  ingredients.remove(doc_ids=[id])


def all_meals():
  return document_id_to_id(*meals.search(Query().meals_remaining > 0))


def save_meal(meal):
  res = meals.insert(dataclasses.asdict(meal))
  return res[0]


def delete_meal(id):
  meals.remove(doc_ids=[id])


def save_favoruite_meal(favoruite_meal):
  res = favourite_meals.upsert(dataclasses.asdict(favoruite_meal), Query().label == favoruite_meal.label)
  return res[0]


def delete_favoruite_meal(id):
  favourite_meals.remove(doc_ids=[id])


def all_favourite_meals():
  regular_meals = all_meals()
  favourites = document_id_to_id(*favourite_meals.all())
  []


def eat_meal(id):
  def eat(doc):
    doc['times_eaten'] = doc['times_eaten'] + [util.date_to_string(datetime.now())]
    doc['meals_remaining'] = doc['meals_remaining'] - 1
    return doc

  meals.update(eat, doc_ids=[id])
  meal = meals.get(doc_id=id)

  today = todays_progress()
  today['meals'] = today['meals'] + [meal]
  today['calories'] = today['calories'] + meal['calories']
  today['protein'] = today['protein'] + meal['protein']

  days_progress.update(today, doc_ids=[today.doc_id])

  return {
    **document_id_to_id(meal)[0],
    **{'progress': today}
  }


def current_goal():
  all_goals = [Goal(calories=g['calories'], protein=g['protein'], from_day=g['from_day']) for g in goals.all()]
  return max(all_goals, key=lambda g: util.string_to_date(g.from_day))


def save_goal(goal):
  current = current_goal()
  if current.calories != goal.calories or current.protein != goal.protein:
    res = goals.upsert(dataclasses.asdict(goal), Query().from_day == goal.from_day)
    return res[0]
  else:
    logger.info('Not updatating goal to %s as it is the same as the current goal %s', goal, current)


def todays_progress():
  today = util.date_to_string(date.today())
  res = days_progress.search(Query().day == today)
  
  if len(res) > 0:
    return res[0]
  else:
    zero = dataclasses.asdict(DayProgress(today, 0, 0))
    days_progress.insert(zero)
    return zero
