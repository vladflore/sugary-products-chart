import time

import pandas as pd

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

start_time = None
foodfacts = None
try:
    print('loading csv...')
    start_time = time.time()
    foodfacts = pd.read_csv('en.openfoodfacts.org.products.csv', sep='\t', low_memory=False)
    print('loaded in', (time.time() - start_time), 'seconds')
    start_time = time.time()
    print('processing csv...')
except FileNotFoundError:
    print(
        '{} seems not to exist, if so download it from >https://de.openfoodfacts.org/data< and put it beside this '
        'python file'.format(
            'en.openfoodfacts.org.products.csv'))
    exit()

product_name_not_null = foodfacts['product_name'].notnull()
sugars_not_null = foodfacts['sugars_100g'].notnull()
sugars_condition1 = foodfacts['sugars_100g'] >= 0
sugars_condition2 = foodfacts['sugars_100g'] <= 100


def arecountriesinlist(countries_to_search_for, countries):
    if countries_to_search_for is None or countries is None:
        return False
    countries_str = str(countries)
    if not countries_str.isalpha():
        return False
    countries_str = countries_str.lower()
    return any(country.lower() in countries_str
               for country in countries_to_search_for)


product_sold_in_countries = foodfacts.apply(
    lambda dataset: arecountriesinlist(['France'], dataset['countries']), axis=1)

res = foodfacts[product_name_not_null & sugars_not_null & sugars_condition1 & sugars_condition2][
    ['code', 'product_name', 'sugars_100g', 'main_category']] \
    .sort_values(['sugars_100g'],
                 ascending=[False])

print('processed in', (time.time() - start_time), 'seconds')

print('writing to sugary_products.csv...')
start_time = time.time()
res.to_csv('sugary_products.csv', header=True, index=False)
print('done writing csv in', (time.time() - start_time), 'seconds')

print('grouping values...')
start_time = time.time()
buckets = '1,25,50,75,100'
diagram = {bucket: 0 for bucket in buckets.split(',')}
for row in res.itertuples(index=False):
    sugar_value = float(row[2])
    if sugar_value <= 1:
        diagram['1'] = diagram.get('1', 0) + 1
    elif (sugar_value > 1) & (sugar_value <= 25):
        diagram['25'] = diagram.get('25', 0) + 1
    elif (sugar_value > 25) & (sugar_value <= 50):
        diagram['50'] = diagram.get('50', 0) + 1
    elif (sugar_value > 50) & (sugar_value <= 75):
        diagram['75'] = diagram.get('75', 0) + 1
    else:
        diagram['100'] = diagram.get('100', 0) + 1
print('done grouping values in', (time.time() - start_time), 'seconds')
print(diagram)
# check correctness
print(sum([x for x in list(diagram.values())]), res.shape[0])

fhand = open('chart.js', 'w')
fhand.write("sugary_products = [\n")
idx = 0
length = len(list(diagram.keys()))
labels = {'1': '[0..1]', '25': '(1..25]', '50': '(25..50]', '75': '(50..75]', '100': '(75..100]'}
for pair in diagram.items():
    fhand.write('[\'' + labels[pair[0]] + '\',' + str(pair[1]) + ']')
    if idx < length - 1:
        fhand.write(",\n")
    idx = idx + 1
fhand.write("\n]\n")
fhand.write('sugary_products_count=' + str(res.shape[0]))
fhand.close()
