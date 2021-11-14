import typing
import sysFunctions
import fileFunctions
import csv
import subprocess

def readFileListData(infoFile: str) -> \
    typing.Tuple[typing.List[str], typing.List[int], typing.List[str],
                 typing.List[str], typing.List[str]]:
    """
    TODO
    """
    
    pass

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
    
    return 0

infoFile = r'/home/linux/Documents/TESTOUT/out_2021-11-12_08-55-43.csv'
outFolder = r'/home/linux/Documents/TESTOUT'
outkbps = 128.0

convertAudioFiles(infoFile, outFolder, outkbps)