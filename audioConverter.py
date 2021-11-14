import typing
import sysFunctions
import fileFunctions
import csv
import subprocess

def readFileListData(infoFile: str) -> \
    typing.Tuple[str, typing.List[str], typing.List[str], typing.List[int],
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
        openBracketIdx = rootFolder.find('(')
        if openBracketIdx > -1:
            rootFolder = rootFolder[openBracketIdx+1:-1]
        
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
    
    return rootFolder, fullName, existFileName, kbps, newFileName, title, artist

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
    
    rootFolder, fullName, existFileName, kbps, newFileName, title, artist = \
        readFileListData(infoFile)
    
    # TODO
    # process files
    # write a CSV output with converted files info
    
    return 0

infoFile = r'/home/linux/Documents/TESTOUT/out_2021-11-14_18-48-48.csv'
outFolder = r'/home/linux/Documents/TESTOUT'
outkbps = 128

convertAudioFiles(infoFile, outFolder, outkbps)
