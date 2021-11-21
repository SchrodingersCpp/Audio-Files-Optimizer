import typing
import sysFunctions
import fileFunctions
import csv
import os
import subprocess

def readFileListData(infoFile: str) -> \
    typing.Tuple[str, str, typing.List[str], typing.List[str], typing.List[int],
                 typing.List[str], typing.List[str], typing.List[str]]:
    """
    TODO
    """
    
    fullName = []
    existFileName = []
    kbps = []
    newFileName = []
    title = []
    artist = []
    
    # read the content of a CSV file
    with open(infoFile, 'r') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        
        # extract the root folder path
        header = next(reader)            # read and skip the header line
        rootFolder = header[0]
        # get first occurrence of root folder opening bracket
        # NOTE: regex was not used because the path can contain brackets
        openBracketIdx = rootFolder.find('(')
        if openBracketIdx > -1:
            rootPath = rootFolder[openBracketIdx+1:-1]
            rootFolder = os.path.split(rootPath)[-1] # get root folder name
        
        for row in reader:
            if len(row) > 8:             # files to process
                processedName = row[8]   # gey a new file name value
                if processedName != '':  # check if a new file name exists
                    fullName.append(row[0])
                    existFileName.append(row[1])
                    kbps.append(row[4])
                    newFileName.append(row[8])
                    title.append(row[9])
                    artist.append(row[10])
    
    return rootPath, rootFolder, fullName, existFileName, kbps, newFileName, \
        title, artist

def createFolders(rootPath: str, rootFolder: str, outFolder: str,
                  fullName: typing.List[str],
                  existFileName: typing.List[str]) -> None:
    """
    TODO
    """
    
    # delete a filename and replace the root folder path with the output path
    for i in range(len(fullName)):
        thePath = fullName[i]
        thePath = thePath.replace(rootPath, os.path.join(outFolder, rootFolder))
        thePath = thePath.replace(existFileName[i], '')
        thePath = thePath[:-1]
        fullName[i] = thePath
    
    # remove duplicates
    fullName = list(set(fullName))
    
    # create folders structure
    for path in fullName:
        os.makedirs(path, exist_ok = True)
    
    return None

def convertAudioFiles(infoFile: str, outFolder: str, outkbps: int) -> None:
    """
    TODO
    """
    
    sysFunctions.limitTracebackInfo(0)     # limit traceback info
    fileFunctions.fileCheck(infoFile)      # check "infoFile" correctness
    fileFunctions.dirCheck(outFolder)      # check "outFolder" correctness
    
    # check "outkbps" argument type provided
    if not isinstance(outkbps, int):
        raise TypeError('"outkbps" must be an integer ' +
                        f'("{type(outkbps)}" was provided)!')
    
    # check whether "outkbps" argument is positive
    if outkbps < 1:
        raise TypeError('"outkbps" must be positive ' +
                        f'("{outkbps}" was provided)!')
    
    ffmpeg = 'ffmpeg'                   # converter command
    sysFunctions.cmdInstalled(ffmpeg)   # check if command is installed
    
    # extract data from a csv file
    rootPath, rootFolder, fullName, existFileName, kbps, newFileName, title, \
        artist = readFileListData(infoFile)
    
    # create output folders
    createFolders(rootPath, rootFolder, outFolder, fullName, existFileName)
    
    # TODO
    # process files with multiprocessing
    # write a CSV output with converted files info
    # ffmpeg -i 01* -vn -sn -dn -map a -codec:a libmp3lame -b:a 128k -map_metadata -1 -metadata Artist="Y D" -metadata Title="Some Name" 99.mp3

    
    return 0

infoFile = r'/home/linux/Documents/TESTOUT/out_2021-11-14_18-48-48.csv'
outFolder = r'/home/linux/Documents/TESTOUT'
outFolder = r'/mnt/Space/OUTPUT'
outkbps = 128

convertAudioFiles(infoFile, outFolder, outkbps)
