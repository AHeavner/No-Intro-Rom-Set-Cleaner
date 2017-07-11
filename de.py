# The purpose of this script is to delete the foreign versions of roms from No Intro rom sets.
# To use it, first extract the files from all of the archives in the rom set. Then change the directory
# variable "dir" to the directory that your extracted roms reside. Open a cmd or terminal in the
# directory that the script exists in and run "python de.py". This script will delete the archives
# at the end so do make sure to extract them first.
# This script is meant to keep USA versions only! If you want to keep different versions then change the "patterns" list.

import os, re, sys, stat, time

# Show help menu if -h argument is specified
if "-h" in sys.argv:
	print("""
	The purpose of this script is to delete the foreign versions of roms from No Intro rom sets
	To use it, first extract the files from all of the archives in the rom set. 
		
	Usage:
	python de.py [-t ~/RomSet] [-h] [-r] [-l] [-p] 
	
	-h	Show the help menu
	-t	The target directory to be cleaned
	-m	Renames outputted files to not contain parenthetical data 
	-c	Clean the MULTIBOOT directory tree of old runs
	-l  Logs data to de.log
	-p  Performs operations and writes to de.log without modifying original data
	""")
	quit()

namePattern = re.compile("(?:\s)*\(.*USA.*\)")
betaPattern = re.compile(".\(.*(Proto|Beta).*\)")
zipPattern = re.compile(".*\.(zip|7z)")

patternObjects = [namePattern, betaPattern, zipPattern]

#Use target argument if specifed otherwise use default
if "-t" in sys.argv:
        dir = sys.argv[sys.argv.index("-l") + 1]
else:
        dir = "F:/Emulators/fgc-snes/roms-c/"

deleted = 0
start_time = time.time()

#The purge function takes a directory and a pattern to search for. If the file name is found, purge sets the
#write permissions of the file and then removes it. An exception is thrown if there is an error.
def purge(dir, patternObjects):
	deleted = 0
	for file in os.listdir(dir):
		if not (patternObjects[0].search(file)) or patternObjects[1].search(file) or patternObjects[2].search(file):
			try:
				os.chmod(os.path.join(dir,file), stat.S_IWRITE | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
				os.remove(os.path.join(dir,file))
				deleted += 1
			except OSError as e:
				print("Failed with:", e.strerror)
				
	return deleted
		
#purgeAll(dir, patterns)
deleted = purge(dir, patternObjects)
total_time = time.time() - start_time

print("{} files were deleted in {:.2f} seconds.".format(deleted, total_time))
input("Press enter to exit.")
