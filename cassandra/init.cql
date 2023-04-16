CREATE KEYSPACE restaurant WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 2};
USE restaurant;
CREATE TYPE ingredient (item text, quantity int, unit text);
CREATE TABLE recipe (name text, cuisine text, category text, ingredients list<frozen<ingredient>>, primary key ((name), cuisine));
CREATE INDEX ON recipe (category);

INSERT INTO recipe (name, cuisine, category, ingredients) VALUES ('Pad_Thai', 'Thai', 'Noodle', [{item: 'noodle', quantity: 125, unit: 'g'}, {item: 'shrimp', quantity: 150, unit: 'g'}, {item: 'brown sugar', quantity: 3, unit: 'tbsp'}]);
INSERT INTO recipe (name, cuisine, category, ingredients) VALUES ('Sashimi', 'Japanese', 'Seafood', [{item: 'rice', quantity: 100, unit: 'g'}, {item: 'salmon', quantity: 50, unit: 'g'}]);
INSERT INTO recipe (name, cuisine, category, ingredients) VALUES ('Chicken_Rice', 'Thai', 'Rice', [{item: 'rice', quantity: 300, unit: 'g'}, {item: 'chicken', quantity: 100, unit: 'g'}]);
INSERT INTO recipe (name, cuisine, category, ingredients) VALUES ('Tom_Yum', 'Thai', 'Soup', [{item: 'shrimp', quantity: 200, unit: 'g'}, {item: 'water', quantity: 500, unit: 'g'}, {item: 'lemon grass', quantity: 10, unit: 'leaves'}]);

SELECT * FROM recipe;
SELECT * FROM recipe WHERE name='Pad_Thai';
SELECT * FROM recipe WHERE category='Noodle';
SELECT token(name), name, cuisine FROM recipe;
