# write a program that finds all files with a given prefix:
# spam000.txt, spam001.txt, spam002.txt...etc, located in a single folder
# and locates any gaps in the numbering.
# e.g. spam001.txt, spam002.txt, spam004.txt (spam003.txt is missing, a gap in the numbering)

#This program locates a gap and renames all the trailing files to fill the gap accordingly.

import os, shutil, random, re
from pathlib import Path

fileRegex = re.compile(r"""
(\w+) #group 1: spam
_	# _
(\d+) #group 2: digits
(.txt) #group 3: extension
""",re.VERBOSE)

#check for gap directory and delete if one is already there.
gapDir = Path('gap')
if gapDir.exists():
	shutil.rmtree(gapDir)
os.mkdir(gapDir)
print("empty 'gap' directory created")

#fill gap directory with spam_xx.txt files
for i in range(15):
	with open(gapDir / f'spam_{i}.txt', "w") as f:
		print(f"'spam_{i}.txt' created")
		#Question: How would you create files with spam000.txt,spam001.txt...spam010.txt format?
		#where the inward zeros get 'replaced' with the current iterator number as listed in the example.

gapDirFiles= gapDir.glob('*')
#As I understand it, this creates a generator object that when called
#will run the code inside the glob method to 'generate' matches from the glob argument.
#each match found is added to a list, and then forgotten as a new match is found.
#once the generator has iterated over the entire list, the generator is 'exhausted'.
#Though the generator object still seems to exist.
# 
# Question1: Is this a decent perception of how generators work?
# Question2: Is there any use for the exhausted generator object?
# Question3: I noticed gapDirFiles 'gi_frame' attribute(correct?) changes to None after the generator is called.
# is that where the generator holds the link to where to generate information from and deletes it once iterated through fully?

pathList = list(gapDirFiles)

#sort list according to regex match object group 2
def sortKey(fileName):
	matchObject = re.search(fileRegex, str(fileName))
	return int(matchObject.group(2))

pathList.sort(key=sortKey)

#delete a random file to create gap
randomFile = random.choice(pathList[1:-1])
os.remove(randomFile)
print(f'{randomFile} deleted.')


fileList = os.listdir(gapDir)
fileList.sort(key= sortKey)

def findGap(listOfFiles):
	startnumber = re.search(fileRegex, str(listOfFiles[0])).group(2)
	startnumber = int(startnumber)

	for i in range(len(listOfFiles)):
		gapCount =  startnumber + i
		currentFileNumber = re.search(fileRegex, str(listOfFiles[i])).group(2)
		currentFileNumber = int(currentFileNumber)
		if gapCount != currentFileNumber:
			return gapCount

gapCount = findGap(fileList)

#close the gap
filesToRename = fileList[gapCount:]
for i in range(len(filesToRename)):
	newDigit = gapCount + i
	currentFile = os.path.join('gap',filesToRename[i])
	newFile = os.path.join('gap',f'spam_{newDigit}.txt')
	os.rename(currentFile, newFile)
	print(f'{currentFile} renamed: {newFile}')