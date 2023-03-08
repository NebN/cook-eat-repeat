CREATE TABLE IF NOT EXISTS ingredient(
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  label TEXT NOT NULL UNIQUE,
  calories DECIMAL NOT NULL,
  proteins DECIMAL NOT NULL,
  serving_size DECIMAL,
  favourite BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS recipe(
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  label TEXT UNIQUE
);


CREATE TABLE IF NOT EXISTS meal(
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  calories DECIMAL NOT NULL,
  protein DECIMAL NOT NULL,
  meals_created INTEGER NOT NULL,
  meals_remaining INTEGER NOT NULL,
  time_created TIMESTAMP NOT NULL default CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meal_ingredient(
  meal_id INTEGER NOT NULL REFERENCES meal(id),
  ingredient_id INTEGER NOT NULL REFERENCES ingredient(id),
  amount_grams INTEGER,
  amount_servings INTEGER,
  PRIMARY KEY (recipe_id, ingredient_id)
);

CREATE TABLE IF NOT EXISTS recipe_ingredient(
  meal_id INTEGER NOT NULL REFERENCES recipe (id),
  ingredient_id INTEGER NOT NULL REFERENCES ingredient(id),
  amount_grams INTEGER,
  amount_servings INTEGER,
  PRIMARY KEY (recipe_id, ingredient_id)
);

CREATE TABLE IF NOT EXISTS meal_eaten(
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  meal_id INTEGER NOT NULL references meal(id),
  time_eaten TIMESTAMP NOT NULL default CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ingredient_view
AS SELECT id, label, calories, proteins, serving_size, favourite, round(cast(proteins as float)*100/cast(calories as float), 2) as protein_ratio
FROM ingredient
ORDER BY protein_ratio DESC;