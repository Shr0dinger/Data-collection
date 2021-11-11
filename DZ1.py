import requests
import json
from pprint import pprint

name = "Shr0dinger"
url = f"https://api.github.com/users/{name}/repos"

resp = requests.get(url)
j_data = resp.json()
GitDat = []

for rep in j_data[:]:
    GitDat.append(rep['name'])

with open("Git_RepFile.json", "w") as write_f:
    json.dump(GitDat, write_f)

with open("Git_RepFile.json", "r") as read_f:
    LoadData = json.load(read_f)
    print(f'List of repositories for user "{name}": {LoadData}')
