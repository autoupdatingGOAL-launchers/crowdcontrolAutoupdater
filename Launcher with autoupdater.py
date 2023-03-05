# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 20:46:07 2022

@author: Zed
"""
from datetime import datetime
from os.path import exists
import json
import os
import pathlib
import zipfile
import progressbar
import requests
import shutil
import subprocess
import urllib


launchUrl ="https://api.github.com/repos/zedb0t/OpenGoal-Crowd-Control-Launcher/releases"  
AppdataPATH = os.getenv('APPDATA') + "\\OpenGOAL-CrowdControl\\"
filename = r"bin/Crowd Control Main Menu.exe"
fileToCheck = AppdataPATH + "\\" + filename

print(fileToCheck)

def copytree(src, dst, overwrite=False):

    if os.path.exists(dst):
        if not overwrite:
            raise OSError(f"Destination directory '{dst}' already exists and overwrite is False")
    else:
        os.makedirs(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, overwrite)
        else:
            shutil.copy2(s, d)

pbar = None
def show_progress(block_num, block_size, total_size):
    if total_size > 0:
        global pbar
        if pbar is None:
            pbar = progressbar.ProgressBar(maxval=total_size)
            pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            pbar.update(downloaded)
        else:
            pbar.finish()
            pbar = None

def try_remove_file(file):
    if exists(file):
        os.remove(file)

def try_remove_dir(dir):
    if exists(dir):
        shutil.rmtree(dir)
        
def downloadNewestmod():
    
    InstallDir = AppdataPATH
    
    
    r = json.loads(json.dumps(requests.get(url = launchUrl, params = {'address':"yolo"}).json()))
    LatestRel = datetime.strptime(r[0].get("published_at").replace("T"," ").replace("Z",""),'%Y-%m-%d %H:%M:%S')
    LatestRelAssetsURL = (json.loads(json.dumps(requests.get(url = r[0].get("assets_url"), params = {'address':"yolo"}).json())))[0].get("browser_download_url")

    LastWrite = datetime(2020, 5, 17)
    if (os.path.exists(fileToCheck)):
        LastWrite = datetime.utcfromtimestamp( pathlib.Path(fileToCheck).stat().st_mtime)

    
    #update checks

    needUpdate = bool((LastWrite < LatestRel))

    print("Currently installed version created on: " + LastWrite.strftime('%Y-%m-%d %H:%M:%S'))
    print("Newest version created on: " + LatestRel.strftime('%Y-%m-%d %H:%M:%S'))

    if (needUpdate):
        
        #start the actual update method if needUpdate is true
        print("Starting Update...")
        #download update from github
        # Create a new directory because it does not exist
        try_remove_dir(AppdataPATH + "/temp")
        if not os.path.exists(AppdataPATH + "/temp"):
            print("Creating install dir: " + AppdataPATH)
            os.makedirs(AppdataPATH + "/temp")

        print("Downloading update from " + LatestRelAssetsURL)
        file = urllib.request.urlopen(LatestRelAssetsURL)
        print()
        print(str("File size is ") + str(file.length))
        urllib.request.urlretrieve(
            LatestRelAssetsURL, InstallDir + "/temp/updateDATA.zip", show_progress
        )
        print("Done downloading")
        
        
        #delete any previous installation
        print("Removing previous installation " + AppdataPATH)
        try_remove_dir(InstallDir + "/data")
        try_remove_file(InstallDir + "/gk.exe")
        try_remove_file(InstallDir + "/goalc.exe")
        try_remove_file(InstallDir + "/extractor.exe")
        print("Extracting update")

        TempDir = InstallDir + "/temp"
        with zipfile.ZipFile(TempDir + "/updateDATA.zip", "r") as zip_ref:
            zip_ref.extractall(InstallDir)

        # delete the update archive
        try_remove_file(TempDir + "/updateDATA.zip")

        #delete the update archive
        try_remove_file(TempDir + "/updateDATA.zip")

        source_dir = InstallDir + '\Release'
        dest_dir = InstallDir

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        files = os.listdir(source_dir)

        for f in files:
            copytree(source_dir, dest_dir, overwrite=True)


        shutil.rmtree(source_dir)

        try_remove_dir(TempDir)

        

if os.path.exists(AppdataPATH) == False:
    print("Creating Directory " + AppdataPATH)
    os.mkdir(AppdataPATH)


downloadNewestmod()


subprocess.call([AppdataPATH + filename])
    
    