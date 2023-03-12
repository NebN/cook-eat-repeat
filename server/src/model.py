import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from src import util


@dataclass
class Ingredient:
  id: int 
  label: str
  calories: Decimal
  proteins: Decimal
  serving_size: Decimal
  favourite: bool = False


@dataclass
class Amount:
  grams: int
  servings: int


@dataclass
class Meal:
  id: int 
  label: str
  ingredients: list[(Ingredient, Amount)]
  calories: Decimal
  protein: Decimal
  meals_created: int
  meals_remaining: int
  time_created: str = util.date_to_string(datetime.datetime.now())
  times_eaten: list[str] = field(default_factory=lambda: [])


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

