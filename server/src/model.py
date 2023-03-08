import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Ingredient:
  id: int
  label: str
  calories: Decimal
  proteins: Decimal # TODO protein
  serving_size: Decimal
  favourite: bool = False


@dataclass
class Recipe:
  id: int
  label: str
  ingredient_ids: list[int]


@dataclass
class RecipeIngredient:
  recipe_id: int
  ingredient_id: int
  amount_grams: int
  amount_servings: int


@dataclass
class Meal:
  id: int
  recipe_id: int
  calories: Decimal
  protein: Decimal
  meals_created: int
  meals_remaining: int
  time_created: datetime.datetime = datetime.datetime.now()


@dataclass
class MealEaten:
  id: int
  id_meal: int
  time_eaten:  datetime.datetime = datetime.datetime.now()