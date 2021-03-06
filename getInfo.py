import sysFunctions
import fileFunctions

def getInfo(folderIn: str, folderOut: str) -> int:
	"""
	Gets file info and writes it to a file.

	folderIn : str
		Folder being processed.

	folderOut: str
		Folder to which an output file is written.

	Returns 0.
	"""

	sysFunctions.limitTracebackInfo(0)	# limit traceback info
	fileFunctions.dirCheck(folderIn)	# check "folderIn" correctness
	fileFunctions.dirCheck(folderOut)	# check "folderOut" correctness

	fileName, fullName = \
		fileFunctions.listFiles(folderIn, True) # list files in directory

	bitrateType, kbps, title, artist = \
		fileFunctions.getMetadata(fullName) # get metadata from filelist

	fileSize	= fileFunctions.getFileSize(fullName) # get the size of the files
	extensions	= fileFunctions.getFileExtension(fileName) # get files extensions

	fileFunctions.writeData(folderIn, fullName, fileName, extensions,
							bitrateType, kbps, title, artist, fileSize,
							folderOut) # write data to a file

	return 0

if __name__ == '__main__':
	folder	= r'/home/linux/Documents/TEST'
	out			= r'/home/linux/Documents/TESTOUT'
	print(getInfo(folder, out))
