import json

fileread = json.loads(open('./models/json/config.json','r',encoding='utf-8').read())

print(fileread)