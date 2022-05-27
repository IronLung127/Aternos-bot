import json

file = open("example.json", "r+")
data = json.loads(file.read(1000))

print(data['age'])