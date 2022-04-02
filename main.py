import yaml
import requests
import json
import os

if not os.path.exists("mods"):
    os.mkdir("mods")

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

mods_to_download = config["mods"]
mc_version = config["mc_version"]

for item in mods_to_download:
    res = requests.get(f"https://api.modrinth.com/v2/project/{item}")

    if not res.ok:
        print(f"{item} not found!")
        continue

    mod_data = json.loads(res.content)

    res = requests.get(f"https://api.modrinth.com/v2/project/{item}/version")

    if not res.ok:
        print(f"{item} versions not found!")
        continue

    mod_versions_data = json.loads(res.content)

    mod_version_to_download = ""
    for mod_version in mod_versions_data:
        if mc_version in mod_version["game_versions"]:
            mod_version_to_download = mod_version
            break

    mod_file = requests.get(mod_version_to_download["files"][0]["url"]).content
    filename = mod_version_to_download["files"][0]["filename"]
    open(f"mods/{filename}", 'wb').write(mod_file)
