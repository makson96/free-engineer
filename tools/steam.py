#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time
from subprocess import Popen

def start(login, password, engineer_dir, s_appid, game_dir):
	os.chdir(engineer_dir)
	if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", engineer_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(engineer_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	if os.path.isfile(engineer_dir+"steam_log.txt") == True:
		os.remove(engineer_dir+"steam_log.txt")
	steam_download = Popen("script -q -c \"./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit\" /dev/null", shell=True, bufsize=1, stdout=open("steam_log.txt", "wb"))
	while steam_download.poll() is None:
		#Terminate the process if bad login or password
		#steam_download.terminate()
		time.sleep(2)

def status(engineer_dir):
	os.chdir(engineer_dir)
	status = "Downloading and installing game data"
	percent = 25
	try:
		steam_log_file = open("steam_log.txt", "r")
		steam_log_lines = steam_log_file.readlines()
		steam_last_line = steam_log_lines[-1]
		steam_log_file.close()
	except:
		steam_last_line = "progress: 0,0 ("
	if "Login Failure" in steam_last_line:
		status = "Error: Steam - bad login or password. Please correct and start again."
		percent = 0
	elif "progress: " in steam_last_line:
		steam_value = steam_last_line.split("progress: ")[1]
		steam_value = steam_value.split(" (")[0]
		steam_value = steam_value.split(",")[0]
		steam_value = int(steam_value) * 70 / 100
		status = "Downloading and installing game data"
		percent = 25 + steam_value
	elif "Success!" in steam_last_line:
		status = "Downloadof game data completed"
		percent = 95
	return status, percent
