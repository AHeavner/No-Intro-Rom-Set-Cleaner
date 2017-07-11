# The purpose of this script is to delete the foreign versions of roms from No Intro rom sets.
# To use it, first extract the files from all of the archives in the rom set. This script 
# will delete the archives at the end so do make sure to extract them first.
#
# This script is meant to keep USA versions only! If you want to keep different versions then change the "patterns" list.

# Authors:
# @AHeavner
# @bpdev97
# Since 7/10/17

import os, re, sys, stat, time

deleted = 0
start_time = time.time()

def reCompiler():
	namePattern = re.compile("(?:\s)*\(.*(USA|World).*\)")
	noNamePattern = re.compile("\(.*\)")
	betaPattern = re.compile(".\(.*(Proto|Beta).*\)")
	zipPattern = re.compile(".*\.(zip|7z)")

	patternObjects = [namePattern, noNamePattern, betaPattern, zipPattern]
	return patternObjects

# Show help menu if -h argument is specified
def helpMenu(args):
	if "-h" in args:
		print("""
		The purpose of this script is to delete the foreign versions of roms from No Intro rom sets
		To use it, first extract the files from all of the archives in the rom set. 
			
		Usage:
		python de.py [-t ~/RomSet] [-h] [-r] [-l] [-p] 
		
		-h  Show the help menu
		-t  The target directory to be cleaned
		-m  Renames outputted files to not contain parenthetical data 
		-l  Logs data to de.log
		-p  Performs operations and writes to de.log without modifying original data
		""")

#Use target argument if specifed otherwise use default
def setTarget(args):
	if "-t" in args:
			dir = args[args.index("-t") + 1]
	else:
			dir = "E:/Emulators/fgc-snes/roms-c/"

def logger(args, log):
	if "-l" in args or "-p" in args:
		logFile = open("de.log", "w")
		logFile.write(log)
		logFile.close()

def message(numDeleted, directory, totaltime):
	if "-p" in sys.argv:
		print("{} files in {} would be deleted!".format(numDeleted, directory))
		input("Press enter to exit.")
	else:
		print("{} files were deleted in {:.2f} seconds.".format(deleted, totaltime))
		input("Press enter to exit.")

def getTimeDelta(startTime):
	return time.time() - startTime

#The purge function takes a directory and a pattern to search for. If the file name is found, purge sets the
#write permissions of the file and then removes it. An exception is thrown if there is an error.
def purge(dir, patternObjects):
	deleted = 0
	log = ""
	for file in os.listdir(dir):
		if not (patternObjects[0].search(file)) or not (patternObjects[1].search(file)) or patternObjects[2].search(file) or patternObjects[3].search(file):
			try:
				if not "-p" in sys.argv:
					os.chmod(os.path.join(dir,file), stat.S_IWRITE | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
					os.remove(os.path.join(dir,file))
				deleted += 1
				log += file + " deleted\n"
			except OSError as e:
				print("Failed with:", e.strerror)

	logger(sys.argv, log)
	return deleted

patternObjects = reCompiler()
helpMenu(sys.argv)
setTarget(sys.argv)
deleted = purge(dir, patternObjects)
total_time = getTimeDelta(start_time)
message(deleted, dir, total_time)

