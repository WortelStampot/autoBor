#Create a gap in a directory of numbered files so a new file can be added.
import shutil, os, re
from pathlib import Path

fileRegex = re.compile(r"""
	(\w+) #group1: spam
	(\d\d\d) #group2: 000-999
	(.txt) #group3: extension
	""",re.VERBOSE)


#check for insertGap folder, make it
def spawnDirectory(path):
	"""spawn an empty directory at path, delete previous incarnation"""
	if path.exists():
		shutil.rmtree(path)
	path.mkdir()
	print(f"emtpy '{path.name}' directory created")


#fill gap directory with x number of files
def fillDirectory(dirPath, numberOfFiles):
	"""fill directory with numberOfFiles"""
	for i in range(numberOfFiles):
		with open(dirPath / f'spam{str(i).zfill(3)}.txt', "w") as f:
			print(f"spam{str(i).zfill(3)}.txt created")


def sortKey(fileName):
	"""sort by int value of digits in file name"""
	matchObject = re.search(fileRegex, str(fileName))
	if int(matchObject.group(2)) == 0:
		return 0
	else:
		return int(matchObject.group(2).lstrip('0')) #strip leading zeros


def insertGap(dirPath, inputNumber):
	"""insert gap at inputNumber"""
	#get all the files in dirPath, and sort the list.
	fileList = os.listdir(dirPath)
	fileList.sort(key = sortKey)
	# rename all the files to the right of the inputNumber
	renameList = fileList[inputNumber:]
	for i in range(len(renameList)):
		newNumber = i + inputNumber + 1
		preGapFile = dirPath / renameList[i]
		postGapFile = dirPath / f"spam{str(newNumber).zfill(3)}.txt"
		os.rename(preGapFile, postGapFile)
		print(f"{preGapFile} renamed: {postGapFile}")
	print(f"Gap created at {inputNumber} ")

path = Path('insertGap')

spawnDirectory(path)

fillDirectory(path, 15)

insertGap(path, 12)
