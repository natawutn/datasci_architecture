#
from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
from google.cloud.bigtable.row_set import RowSet

import os
import datetime
import json

# indicate the localtion of our local emulator
os.environ['BIGTABLE_EMULATOR_HOST'] = 'localhost:8086'

# dummy project and instance
project_id = 'dsa_test'
instance_id = 'restaurant'
table_id = 'recipe'

# connect to the local emulator
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)

# create table if not exists
if not table.exists():
    # Create a column family with GC policy : most recent N versions
    # Define the GC policy to retain only the most recent 1 version
    max_versions_rule = column_family.MaxVersionsGCRule(1)
    column_families = {'general': max_versions_rule, 'ingredients': max_versions_rule}
    table.create(column_families=column_families)

# our data
all_dishes = [
    {'name': 'Pad_Thai', 'cuisine': 'Thai', 'general': {'category': 'Noodle'}, 'ingredients': [{'item': 'noodle', 'quantity': 125, 'unit': 'g'}, {'item': 'shrimp', 'quantity': 150, 'unit': 'g'}, {'item': 'brown sugar', 'quantity': 3, 'unit': 'tbsp'}]},
    {'name': 'Sashimi', 'cuisine': 'Japanese', 'general': {'category': 'Seafood'}, 'ingredients': [{'item': 'rice', 'quantity': 100, 'unit': 'g'}, {'item': 'salmon', 'quantity': 50, 'unit': 'g'}]},
    {'name': 'Chicken_Rice', 'cuisine': 'Thai', 'general': {'category': 'Rice'}, 'ingredients': [{'item': 'rice', 'quantity': 300, 'unit': 'g'}, {'item': 'chicken', 'quantity': 100, 'unit': 'g'}]},
    {'name': 'Tom_Yum', 'cuisine': 'Thai', 'general': {'category': 'Soup'}, 'ingredients': [{'item': 'shrimp', 'quantity': 200, 'unit': 'g'}, {'item': 'water', 'quantity': 500, 'unit': 'g'}, {'item': 'lemon grass', 'quantity': 10, 'unit': 'leaves'}]}
]

# populate the table
rows = []
for dish in all_dishes:
    now = datetime.datetime.utcnow()
    # use cuisine#name as a row key pattern
    row_key = '{}#{}'.format(dish['cuisine'], dish['name']).encode()
    row = table.direct_row(row_key)
    value = dish['general']['category'].encode('utf-8')
    row.set_cell('general', 'category'.encode(), value, timestamp=now)
    for i, val in enumerate(dish['ingredients']):
        col = str(i).encode()
        value = json.dumps(val).encode('utf-8')
        row.set_cell('ingredients', col, value, timestamp=now)
    rows.append(row)
table.mutate_rows(rows)


# our print row function
def print_row(row):
    row_key = row.row_key.decode('utf-8')
    category = row.cells['general']['category'.encode()][0].value.decode("utf-8")
    ingredients = row.cells['ingredients']
    l = []
    for col in ingredients:
        value = ingredients[col][0].value.decode('utf-8')
        l.append(value)
    print('{}:'.format(row_key))
    print('  category = {}'.format('category'))
    print('  ingredients = [{}]'.format(','.join(l)))


# we want each cell to return only the latest version
row_filter = row_filters.CellsColumnLimitFilter(1)

# read a single row by row_key
print('Reading Pad Thai:')
row_key = 'Thai#Pad_Thai'.encode()
row = table.read_row(row_key, row_filter)
print_row(row)
print('----------')

# scan all rows
print('Scanning for all dishes:')
partial_rows = table.read_rows(filter_=row_filter)

for row in partial_rows:
    print_row(row)
print('----------')

print('Scanning for all Thai dishes:')
# Create a filter to only retrieve all Thai cuisine
prefix = "Thai#"
end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)
row_set = RowSet()
row_set.add_row_range_from_keys(prefix.encode("utf-8"), end_key.encode("utf-8"))
partial_rows = table.read_rows(row_set=row_set, filter_=row_filter)

for row in partial_rows:
    print_row(row)