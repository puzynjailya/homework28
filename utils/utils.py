import json
import csv
import os
from typing import Dict, Any

datasets_path = '..\datasets'
fixtures_path = '..\\fixtures'

models = {'ad.csv': 'advertisements.advertisement',
          'category.csv': "advertisements.category",
          'location.csv': "users.location",
          "user.csv": "users.user"}

ads_filename = 'ad.csv'
categories_filename = 'category.csv'


def csv_to_json(datasets_path, file_path):
    result = []

    # Читаем csv файл и получаем данные из него
    with open(os.path.join(datasets_path, file_path), encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            data = {}
            rows['id'] = int(rows['id'])
            if file_path == 'ads.csv':
                rows['is_published'] = rows['is_published'].capitalize()
            data['pk'] = int(rows['id'])
            data['model'] = models.get(file_path)
            data['fields'] = rows
            result.append(data)

    # Сохраняем данные в json файл
    with open(os.path.join(fixtures_path, file_path[:-4] + '.json'), 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    files = [ads_filename, categories_filename]
    for filename in os.listdir(datasets_path):
        csv_to_json(datasets_path, filename)


