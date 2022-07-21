import json
import csv
import os
from typing import Dict, Any

datasets_path = '..\datasets'
fixtures_path = '..\\fixtures'

models = {'ad.csv': 'advertisements.advertisement',
          'category.csv': "categories.category",
          'location.csv': "users.location",
          "user.csv": "users.user"
          }


def csv_to_json(datasets_path, file_path):
    result = []

    # Читаем csv файл и получаем данные из него
    with open(os.path.join(datasets_path, file_path), encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            data = {}
            rows['id'] = int(rows['id'])

            if file_path == 'ad.csv':
                rows['is_published'] = rows['is_published'].capitalize()

            if file_path == 'user.csv':
                rows['age'] = int(rows['age'])
                rows['location_id'] = int(rows['location_id'])
            if file_path == 'location.csv':
                rows['lat'], rows['lng'] = float(rows['lat']), float(rows['lng'])

            data['pk'] = int(rows['id'])
            data['model'] = models.get(file_path)
            data['fields'] = rows
            result.append(data)

    # Сохраняем данные в json файл
    with open(os.path.join(fixtures_path, file_path[:-4] + '.json'), 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)


def create_m2mtable(datasets_path, file_path):
    loc_ids = []
    model_data = {"user.csv": "users.user.location"}

    # Читаем csv файл и получаем данные из него
    with open(os.path.join(datasets_path, file_path), encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            result = {}
            data = {}
            result['user_id'] = int(rows['id'])
            result['location_id'] = int(rows['location_id'])

            data['pk'] = int(rows['id'])
            data['model'] = model_data.get(file_path)
            data['fields'] = result
            loc_ids.append(data)
    # Сохраняем данные в json файл
    with open(os.path.join(fixtures_path, 'locations.json'), 'w', encoding='utf-8') as json_file:
        json.dump(loc_ids, json_file, ensure_ascii=False, indent=4)


def csv_locations_create(datasets_path, file_path):
    with open(os.path.join(datasets_path, file_path), encoding='utf-8') as csv_file:
        result = [['id', 'user_id', 'location_id']]
        csv_reader = csv.DictReader(csv_file)
        included_cols=['id', 'location_id']
        for row in csv_reader:
            content = [row['id']]
            content.extend(row[i] for i in included_cols)
            result.extend(content)
    with open(os.path.join(datasets_path, 'locs.csv'), 'w', encoding='utf-8') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(result)

if __name__ == '__main__':
    for filename in os.listdir(datasets_path):
        csv_to_json(datasets_path, filename)
        if filename == 'user.csv':
            create_m2mtable(datasets_path, filename)
    csv_locations_create(datasets_path, 'user.csv')




