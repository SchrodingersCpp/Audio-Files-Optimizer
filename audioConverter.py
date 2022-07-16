import typing
import sysFunctions
import fileFunctions
import getInfo
import csv
import os
import subprocess
import multiprocessing

def readFileListData(infoFile: str) -> \
	typing.Tuple[str, str, typing.List[str], typing.List[str], typing.List[str],
				 typing.List[str], typing.List[str], typing.List[str]]:
	"""
	Reads files data from a csv file.

	infoFile : str
		A csv file containing infromation about files.

	Returns:
		Path to input root folder : str.
		Input root folder name : str.
		List of input file full names : List[str].
		List of input file names : List[str].
		List of input file kbps : List[str].
		List of converted file names : List[str].
		List of converted file titles : List[str].
		List of converted file artists : List[str].
	"""

	fullName		= []
	existFileName	= []
	kbps			= []
	newFileName		= []
	title			= []
	artist			= []

	# read the content of a CSV file
	with open(infoFile, 'r') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')

		# extract the root folder path
		header = next(reader)			# read and skip the header line
		rootFolder = header[0]

		# get first occurrence of root folder opening bracket
		# NOTE: regex was not used because the path may contain brackets
		openBracketIdx = rootFolder.find('(')
		if openBracketIdx > -1:
			rootPath = rootFolder[openBracketIdx+1:-1]
			rootFolder = os.path.split(rootPath)[-1] # get root folder name

		for row in reader:
			if len(row) > 8:			# files to process
				processedName = row[8]	# gey a new file name value
				if processedName != '':	# check if a new file name exists
					fullName.append(row[0])
					existFileName.append(row[1])
					kbps.append(row[4])
					newFileName.append(row[8])
					title.append(row[9])
					artist.append(row[10])

	return rootPath, rootFolder, fullName, existFileName, kbps, newFileName, \
		title, artist

def createFolders(rootPath		: str, rootFolder	: str,
				  outFolder		: str, fullName		: typing.List[str],
				  existFileName	: typing.List[str]) -> typing.List[str]:
	"""
	Creates output folder hierarchy.

	rootPath : str
		Input folder path.

	rootFolder : str
		Input folder name.

	outFolder : str
		Output folder path.

	fullName : List[str]
		List of input file full names.

	existFileName : List[str]
		List of input file names.

	Returns:
		List of output folders : List[str].
	"""

	# delete a filename and replace the root folder path with the output path
	outPaths = []
	for i in range(len(fullName)):
		thePath = fullName[i]
		thePath = thePath.replace(rootPath, os.path.join(outFolder, rootFolder))
		thePath = thePath.replace(existFileName[i], '')
		thePath = thePath[:-1]
		outPaths.append(thePath)

	# remove duplicates
	setOutFolders = list(set(outPaths))

	# create folders structure
	for path in setOutFolders:
		os.makedirs(path, exist_ok=True)

	return outPaths

def convertAudioFile(fileFullName	: str, fileExistkbps	: str,
					 fileOutFolder	: str, fileNewName		: str,
					 fileArtist		: str, fileTitle		: str,
					 newkbps		: int,
					 mOutput) -> None:
	"""
	Converts an audio file to MP3 format, reduces kbps,
		removes all tags and album art, and adds Artist and Title tags.

	fileFullName : str
		Input file name.

	fileExistkbps : str
		Input file kbps.

	fileOutFolder : str
		Converted file folder.

	fileNewName : str
		Converted file name.

	fileArtist : str
		Converted file artist.

	fileTitle : str
		Converted file artist.

	newkbps : int
		Converted file kbps.

	mOutput : multiprocessing manager
		Output manager storying input file name, converted file name,
			converted binary output, binary output error.

	Returns None.
	"""

	# if input file doesn't contain kbps info
	if fileExistkbps == '':
		fileExistkbps = 0

	# converter command
	if newkbps > float(fileExistkbps): # for smaller existing kbps ...
		if fileFullName[-4:] == '.mp3': # ... copy audio
			cmd = ['ffmpeg', '-i', 'pipe:0', '-vn', '-sn', '-dn',
				   '-map', 'a', '-codec:a', 'copy',
				   '-map_metadata', '-1',
				   '-metadata', f'Artist={fileArtist}',
				   '-metadata', f'Title={fileTitle}',
				   '-f', 'mp3', 'pipe:1']
		else: # ... convert to new filetype
			cmd = ['ffmpeg', '-i', 'pipe:0', '-vn', '-sn', '-dn',
				   '-map', 'a', '-codec:a', 'libmp3lame', '-b:a',
				   f'{fileExistkbps}k',
				   '-map_metadata', '-1',
				   '-metadata', f'Artist={fileArtist}',
				   '-metadata', f'Title={fileTitle}',
				   '-f', 'mp3', 'pipe:1']
	else: # reduce kbps (convert with new kbps)
		cmd = ['ffmpeg', '-i', 'pipe:0', '-vn', '-sn', '-dn',
			   '-map', 'a', '-codec:a', 'libmp3lame', '-b:a', f'{newkbps}k',
			   '-map_metadata', '-1',
			   '-metadata', f'Artist={fileArtist}',
			   '-metadata', f'Title={fileTitle}',
			   '-f', 'mp3', 'pipe:1']

	# read file to input stream
	cmdout = subprocess.run(['cat', f'{fileFullName}'], stdout=subprocess.PIPE)
	# convert file
	cmdout = subprocess.run(cmd, input=cmdout.stdout,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE)
	output = cmdout.stdout
	outerr = cmdout.stderr

	# get converted file's full path
	outputFullName = os.path.join(fileOutFolder, fileNewName+'.mp3')

	mOutput.append((fileFullName, outputFullName, output, outerr))

	return None

def writeConvertedFiles(logFile: str, fullName_Data:
						typing.List[typing.Tuple[str, str, bytes, bytes]]) \
	-> None:
	"""
	Writes converted files to disk and creates a LOG file with errors.

	logFile : str
		LOG file full path.

	fullName_Data : multiprocessing manager
		Manager storying input file name, converted file name,
			converted binary output, binary output error.

	Returns None.
	"""

	for oldFullName, fullName, data, err in fullName_Data:
		if len(data) == 0: # no converted file stream (error)
			print(f'"{oldFullName}" was not converted!')
			with open(logFile, 'a') as log:
				log.write('\t')
				log.write(oldFullName)
				log.write('\n')
				log.write(err.decode('utf-8'))
				log.write('\n'*2)
		else: # converted file stream
			with open(fullName, 'wb') as outFile:
				outFile.write(data)

	return None

def convertAudioFiles(infoFile: str, outFolder: str, outkbps: int) -> None:
	"""
	Converts audio files and write a CSV file with information
		about converted files.

	infoFile: str
		Input CSV file full path.

	outFolder: str
		Output folder.

	outkbps: int
		Output kbps.

	Returns 0.
	"""

	sysFunctions.limitTracebackInfo(0)	# limit traceback info
	fileFunctions.fileCheck(infoFile)	# check "infoFile" correctness
	fileFunctions.dirCheck(outFolder)	# check "outFolder" correctness

	# check "outkbps" argument type provided
	if not isinstance(outkbps, int):
		raise TypeError('"outkbps" must be an integer ' +
						f'("{type(outkbps)}" was provided)!')

	# check whether "outkbps" argument is positive
	if outkbps < 1:
		raise TypeError('"outkbps" must be positive ' +
						f'("{outkbps}" was provided)!')

	ffmpeg = 'ffmpeg'					# converter command
	sysFunctions.cmdInstalled(ffmpeg)	# check if command is installed

	# extract data from a csv file
	rootPath, rootFolder, fullName, existFileName, kbps, \
		newFileName, title, artist = readFileListData(infoFile)

	# create output folders
	outFolders = createFolders(rootPath, rootFolder, outFolder, fullName,
							   existFileName)

	# get number of CPU physical cores
	nPhysCores = sysFunctions.nPhysicalCores()

	# set number of processes
	nProcs = nPhysCores

	mOutput = multiprocessing.Manager().list() # store outputs

	# create empty log-file for writing errors for not converted files
	logFile = os.path.join(outFolder, 'LOG'+sysFunctions.getTimeStamp())
	open(logFile, 'wb').close()

	totalFiles = len(fullName) # total number of files

	# start processing
	for i in range(0, totalFiles, nProcs):
		chunkSlice			= slice(i, i+nProcs) # chunk range

		# create chunks
		chunkFullName		= fullName[chunkSlice]
		chunkkbps			= kbps[chunkSlice]
		chunkOutFolders		= outFolders[chunkSlice]
		chunkNewFileName	= newFileName[chunkSlice]
		chunkTitle			= title[chunkSlice]
		chunkArtist			= artist[chunkSlice]

		print(f'Processing files {i+1}-{i+len(chunkkbps)} of {totalFiles}.')

		mOutput[:] = [] # empty output list

		# create processes
		procs = []
		for j in range(len(chunkFullName)):
			proc = multiprocessing.Process(target=convertAudioFile,
										   args=(chunkFullName[j],
												 chunkkbps[j],
												 chunkOutFolders[j],
												 chunkNewFileName[j],
												 chunkArtist[j],
												 chunkTitle[j],
												 outkbps,
												 mOutput))
			procs.append(proc)

		for proc in procs:
			proc.start()

		for proc in procs:
			proc.join()

		# write converted files and log on errors
		writeConvertedFiles(logFile, list(mOutput))

	# write a CSV output with converted files info in root folder
	getInfo.getInfo(os.path.join(outFolder, rootFolder), outFolder)

	return 0

if __name__ == '__main__':
	infoFile	= r'/mnt/Space/OUTPUT/out_2021-11-28_16-03-49.csv'
	outFolder	= r'/mnt/Space/OUTPUT'
	outkbps		= 128

	print(convertAudioFiles(infoFile, outFolder, outkbps))
