import subprocess
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import os
import random
import json

def get_metadata():
    '''
    Load metadata from file if exists, otherwise download from dataverse
    '''
    if os.path.isfile('metadata.json'):
        with open('metadata.json','r') as f:
            data=json.load(f)
    else:
        import requests
        url = "https://dataverse.nl/api/datasets/:persistentId/?persistentId=doi:10.34894/AECRSD"
        response = requests.get(url)
        data = response.json()
        with open('metadata.json','w') as f:
            json.dump(data,f)
    return data

def download_file(file_json, local_folder_path):
    '''
    Download a file from dataverse to local folder
    '''
    file_lpath = local_folder_path / Path(file_json.get('directoryLabel', '')) / file_json['dataFile']['filename']
    if file_lpath.exists():
        return
    os.makedirs(file_lpath.parent, exist_ok=True)
    curl_cmd = [
        'curl', '-s', '-L', '-o', file_lpath,
        f'https://dataverse.nl/api/access/datafile/{file_json["dataFile"]["id"]}'
    ]
    result = subprocess.run(curl_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    with open('download.log', 'a') as f:
        f.write(f'Downloaded {file_lpath}: {result.stderr.decode()}\n')

def download_dataset(data, local_folder_path):
    '''
    Download dataset from dataverse to local folder
    '''
    files = data['data']['latestVersion']['files']
    random.shuffle(files)
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(tqdm(executor.map(
            lambda f: download_file(f, local_folder_path), files),
            total=len(files),
            desc="Downloading",
            unit="file"))

if __name__ == "__main__":
    # Get metadata
    data = get_metadata()

    # Folder path
    local_folder_path = Path('/Users/hsuh/Gitrepo/SwitchSite/1.data/MICCAI-2017')

    # Download dataset
    download_dataset(data, local_folder_path)