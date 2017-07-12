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

patternObjects = [
	re.compile("(?:\s)*\(.*(USA|World).*\)"), # Script does not delete files that match this regex
	re.compile("\(.*\)"),                     # Does not delete files that do not have a tag
	re.compile(".\(.*(Proto|Beta).*\)"),      # Does delete files that are prototypes or betas
	re.compile(".*\.(zip|7z)"),               # Deletes leftover archives
	re.compile("([\w\s\&\-$,!'\.+\~]+)(\(.*\)\s*?)?(\.\w*)"),
	re.compile("\(Rev [\w\d\s]+\)")
]

# Show help menu if -h argument is specified
def helpMenu():
	if "-h" in sys.argv:
		print("""
		The purpose of this script is to delete the foreign versions of roms from No Intro rom sets
		To use it, first extract the files from all of the archives in the rom set. 
			
		Usage:
		python de.py [-t ~/RomSet] [-h] [-r] [-l] [-p] 
		
		-h  Show the help menu
		-t  The target directory to be cleaned
		-m  Renames outputted files to not contain parenthetical data 
		-l  Logs data to de.log
		""")

# Use target argument if specifed otherwise use default
def setTarget():
	if "-t" in sys.argv:
			dir = sys.argv[sys.argv.index("-t") + 1]
	else:
			dir = "E:/Emulators/fgc-nes/roms-c/"
	return dir

# Writes deletion log to de.log file
def logger(log):
	if "-l" in sys.argv or "-p" in sys.argv:
		logFile = open("de.log", "w")
		logFile.write(log)
		logFile.close()
# Displays a message about files deleted and time taken
def message(numDeleted, totalTime):
	print("{} files were deleted in {:.2f} seconds.".format(numDeleted, totalTime))
	input("Press enter to exit.")

# Calculates the time delta between the startTime argument and call of this function
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
				os.chmod(os.path.join(dir,file), stat.S_IWRITE | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
				os.remove(os.path.join(dir,file))
				deleted += 1
			except OSError as e:
				print("Failed with:", e.strerror)
	return deleted

def preview(dir):
	deleted = 0
	log = ""
	for file in os.listdir(dir):
		if not (patternObjects[0].search(file)) or not (patternObjects[1].search(file)) or patternObjects[2].search(file) or patternObjects[3].search(file):
			deleted += 1
			log += "Deleted: " + file + "\n"
	print("{} files in {} would be deleted!".format(deleted, dir))
	return log

def purgeAndPreview(dir, patternObjects, startTime):
	log = preview(dir)
	deleted = 0
	if(input("Would you like to delete these files? (yes/no):") == "yes"):
		deleted = purge(dir, patternObjects)
		if "-r" in sys.argv:
			log = rename(dir, log)
		message(deleted, getTimeDelta(startTime))
	logger(log)

def rename(dir, log):
	for file in os.listdir(dir):
		matchFull = re.search(patternObjects[4], file)
		matchRev = re.search(patternObjects[5], file)
		if matchRev:
			os.rename(os.path.join(dir, file), os.path.join(dir, matchFull.group(1).strip() + " " + matchRev.group(0) + matchFull.group(3).strip()))
			log += "Renaming: " + file + " to \n          " + matchFull.group(1).strip() + " " + matchRev.group(0) + matchFull.group(3).strip() + "\n"
		elif matchFull:
			os.rename(os.path.join(dir, file), os.path.join(dir, matchFull.group(1).strip() + matchFull.group(3).strip()))
			log += "Renaming: " + file + " to \n          " + matchFull.group(1).strip() + matchFull.group(3).strip() + "\n"
		else:
			log += "Skipping: " + file + "\n"
	return log

helpMenu()
dir = setTarget()
purgeAndPreview(dir, patternObjects, start_time)