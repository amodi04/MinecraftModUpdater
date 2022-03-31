import yaml
import requests
import json
import os

if not os.path.exists("mods"):
    os.mkdir("mods")

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

mc_version = config["mc_version"]

for mod in config["mods"]:
    res = requests.get(f"https://api.modrinth.com/v2/project/{mod}")

    if res.status_code != 200:
        print(f"{mod} not found!")
        continue

    data = json.loads(res.text)
    get_versions = requests.get(f"https://api.modrinth.com/v2/project/{mod}/version").text
    get_versions = json.loads(get_versions)

    file_version_to_use = ""
    for i in get_versions:
        if mc_version in i["game_versions"]:
            file_version_to_use = i
            break

    game_file = requests.get(file_version_to_use["files"][0]["url"])
    open(f"mods/{mod}-{file_version_to_use['version_number']}.jar", 'wb').write(game_file.content)
