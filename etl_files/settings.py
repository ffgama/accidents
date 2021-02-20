import json

with open('../settings.json') as json_file:
    json = json.load(json_file)
    
MAIN_URL = json.get('MAIN_URL')