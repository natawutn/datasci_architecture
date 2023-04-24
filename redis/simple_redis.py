#
import redis

redis_host = 'localhost'
rd = redis.Redis(host=redis_host)

# our data
all_dishes = [
    {'name': 'Pad_Thai', 'cuisine': 'Thai', 'general': {'category': 'Noodle'}, 'ingredients': [{'item': 'noodle', 'quantity': 125, 'unit': 'g'}, {'item': 'shrimp', 'quantity': 150, 'unit': 'g'}, {'item': 'brown sugar', 'quantity': 3, 'unit': 'tbsp'}]},
    {'name': 'Sashimi', 'cuisine': 'Japanese', 'general': {'category': 'Seafood'}, 'ingredients': [{'item': 'rice', 'quantity': 100, 'unit': 'g'}, {'item': 'salmon', 'quantity': 50, 'unit': 'g'}]},
    {'name': 'Chicken_Rice', 'cuisine': 'Thai', 'general': {'category': 'Rice'}, 'ingredients': [{'item': 'rice', 'quantity': 300, 'unit': 'g'}, {'item': 'chicken', 'quantity': 100, 'unit': 'g'}]},
    {'name': 'Tom_Yum', 'cuisine': 'Thai', 'general': {'category': 'Soup'}, 'ingredients': [{'item': 'shrimp', 'quantity': 200, 'unit': 'g'}, {'item': 'water', 'quantity': 500, 'unit': 'g'}, {'item': 'lemon grass', 'quantity': 10, 'unit': 'leaves'}]}
]

# populate data
id = 101
for dish in all_dishes:
    key = 'dish:{}'.format(id)
    o = {'id': id, 'name': dish['name'], 'cuisine': dish['cuisine'], 'category': dish['general']['category']}
    rd.hset(key, mapping=o)
    key = 'd_ing:{}'.format(id)
    for ingredient in dish['ingredients']:
        ing_str = '{};{};{}'.format(ingredient['item'], ingredient['quantityrd'], ingredient['unit'])
        rd.sadd(key, ing_str)
    id += 1