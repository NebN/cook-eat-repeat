import datetime
import dataclasses
from dataclasses import dataclass, field
from decimal import Decimal
from src import util
from abc import ABC


@dataclass
class Record():
  def to_dict(self):
    return dataclasses.asdict(self)

@dataclass
class Ingredient(Record):
  label: str
  calories: Decimal
  protein: Decimal
  serving_size: Decimal
  favourite: bool = False


@dataclass
class Amount(Record):
  grams: int
  servings: int
  per_meal: bool = False


@dataclass
class Meal(Record):
  label: str
  ingredients: list[(Ingredient, Amount)]
  calories: Decimal
  protein: Decimal
  meals_remaining: int
  time_created: str = util.date_to_string(datetime.datetime.now())
  favourite: bool = False

  def to_dict(self):
    def pop_favourite(ingredient_amount):
      ingredient, amount = ingredient_amount
      ingredient_dict = ingredient.to_dict()
      ingredient_dict.pop('favourite', None)
      return (ingredient_dict, amount.to_dict())

    ingredients_trimmed = [pop_favourite(i) for i in self.ingredients]
    return dataclasses.asdict(dataclasses.replace(self, ingredients=ingredients_trimmed))


@dataclass
class Goal:
  calories: Decimal
  protein: Decimal
  from_day: datetime.date = util.date_to_string(datetime.date.today())


@dataclass
class DayProgress:
  day: datetime.date
  calories: Decimal
  protein: Decimal
  meals: list[Meal] = field(default_factory=lambda: [])

  def to_dict(self):
    def pop_favourite(meal):
      meal_dict = meal.to_dict()
      meal_dict.pop('favourite', None)
      return meal_dict

    meals_trimmed = [pop_favourite(i) for i in self.meals]
    return dataclasses.asdict(dataclasses.replace(self, meals=meals_trimmed))

