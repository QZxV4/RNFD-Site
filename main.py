import requests
import re
import os
from urllib.parse import urlparse
from time import sleep

API_KEY = '$2a$10$h.wwR1Fv0RlxMGQkTmmwles4.lByQ.E0Z2Lntb32wxu3dHdhdguhi'  # Replace with your API key
HEADERS = {'x-api-key': API_KEY}

MINECRAFT_VERSION = '1.20.1'
MODLOADER_NAME = 'Fabric'
GAME_ID = 432  # Minecraft

# Read mod page URLs from a file
with open('mod_links.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

def extract_slug(url):
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) >= 3 and parts[1] == 'mc-mods':
        return parts[2]  # The slug
    return None

def get_project_id(slug):
    url = f'https://api.curseforge.com/v1/mods/search?gameId={GAME_ID}&searchFilter={slug}'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Failed to get ID for {slug}")
        return None
    results = resp.json()['data']
    for mod in results:
        if mod['slug'] == slug:
            return mod['id']
    return None

def get_compatible_file(project_id):
    url = f'https://api.curseforge.com/v1/mods/{project_id}/files'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Failed to get files for project ID {project_id}")
        return None
    files = resp.json()['data']
    for file in files:
        if file['releaseType'] == 3 or file['isServerPack']:
            continue
        if MINECRAFT_VERSION in file['gameVersions']:
            # Check for Fabric specifically
            if any('fabric' in v.lower() for v in file['gameVersions']):
                return file['downloadUrl'], file['fileName']
    return None

# Create output folder
os.makedirs('mods', exist_ok=True)

# Process each mod
for url in urls:
    slug = extract_slug(url)
    if not slug:
        print(f"❌ Invalid CurseForge URL: {url}")
        continue

    print(f"🔍 Searching for mod: {slug}")
    project_id = get_project_id(slug)
    if not project_id:
        print(f"❌ Could not find project ID for {slug}")
        continue

    result = get_compatible_file(project_id)
    if not result:
        print(f"⚠️ No compatible Fabric version for 1.20.1 found for {slug}")
        continue

    download_url, filename = result
    print(f"⬇️ Downloading: {filename}")
    response = requests.get(download_url)
    with open(os.path.join('mods', filename), 'wb') as f:
        f.write(response.content)

    sleep(1)  # Be nice to CurseForge's servers

print("\n✅ Download complete. Mods saved in the 'mods' folder.")
