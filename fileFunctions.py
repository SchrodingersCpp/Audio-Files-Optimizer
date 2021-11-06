import sysFunctions
import typing
import os
import subprocess
import re

def pathChecks(path: str):
    """
    Performs correctness checks for the specified path.
    
    path : str
        Path to the specified folder.
    
    Returns None.
    """
    
    # check "path" argument type provided
    if not isinstance(path, str):
        raise TypeError('"path" must be a string ' +
                        f'("{type(path)}" was provided)!')
    
    # check whether "path" exists
    if not os.path.exists(path):
        raise Exception(f'Specified "path" ("{path}") does not exist!')
    
    return None

def dirCheck(path: str):
    """
    Performs whether the specified path is a directory.
    
    path : str
        Path to the specified folder.
    
    Returns None.
    """
    
    # check path correctness
    pathChecks(path)
    
    # check whether "path" is a folder
    if not os.path.isdir(path):
        raise Exception(f'Specified "path" ("{path}") is not a folder!')
    
    return None

def fileCheck(path: str):
    """
    Performs whether the specified path is a file.
    
    path : str
        Path to the specified file.
    
    Returns None.
    """
    
    # check path correctness
    pathChecks(path)
    
    # check whether "path" is a file
    if not os.path.isfile(path):
        raise Exception(f'Specified "path" ("{path}") is not a file!')
    
    return None

def listFiles(path: str, recursive: bool = False) -> \
    typing.Tuple[typing.List[str], typing.List[str]]:
    """
    Lists files in the specified folder.
    
    path : str
        Path to the specified folder.
    
    recursive : bool
        Specifies whether to list files recursively.
        Defaults to False (do not check folders recursively).
    
    Returns:
        List of file names : List[str].
        List of full path to the files : List[str].
    """
    
    # check "recursive" argument type provided
    if not isinstance(recursive, bool):
        raise TypeError('"recursive" must be a boolean ' +
                        f'("{type(recursive)}" was provided)!')
    
    fileName = [] # file names only
    fullName = [] # file full names
    if recursive is True: # list files in the dir and subdirs
        for root, dirs, files in os.walk(path):
            for file in files:
                fileName.append(file)
                fullName.append(os.path.join(root, file))
    else: # list files in the dir only
        for file in os.listdir(path):
            fullPath = os.path.join(path, file)
            if os.path.isfile(fullPath):
                fileName.append(file)
                fullName.append(fullPath)
    
    return fileName, fullName

def getMetadata(files: typing.List[str]) -> \
    typing.Tuple[typing.List[str], typing.List[str],
                 typing.List[str], typing.List[str]]:
    """
    TODO
    Add function description
    """
    
    fileInfoCmd = 'mediainfo'               # file info command
    sysFunctions.cmdInstalled(fileInfoCmd)  # check if command is installed
    
    bitrateType = []
    kbps = []
    title = []
    artist = []
    
    # keywords to find appropriate info
    keyAudio = 'audio'                  # used to check if it is audio
    keyBitrateType = 'bit.rate mode'
    keykbps = 'bit.rate'
    keykbpsUnit = 'kb.s'
    keyTitle = 'track name'
    keyArtist = 'performer'
    
    nNP = 0 # count not processed files
    
    for file in files:
        fileCheck(file) # check if the file exists
        metadata = subprocess.run([fileInfoCmd, file],
                                  stdout = subprocess.PIPE) # get metadata
        metadata = metadata.stdout.decode('utf-8')
        if keyAudio not in metadata.lower(): # if not an audio file
            nNP += 1
            print(f'{(str(nNP)+":").ljust(5)} "{file}" does not contain audio!')
            
            bitrateType.append('')
            kbps.append('')
            title.append('')
            artist.append('')
            
        else: # if an audio file
            # get Audio section
            
            audioMetadata = metadata[re.search(f'^{keyAudio}$', metadata,
                            flags = re.MULTILINE | re.IGNORECASE).start():]
            
            # get bitrate mode
            result = re.findall(rf'^.*{keyBitrateType}.*$', audioMetadata,
                                flags = re.MULTILINE | re.IGNORECASE)
            if result != []:
                result = result[0]
                result = re.findall(r":.*", result)[0]
                result = result[1:].strip()
                bitrateType.append(result)
            else:
                bitrateType.append('')
            
            # get kbps
            result = re.findall(rf'^.*{keykbps}.*$', audioMetadata,
                                flags = re.MULTILINE | re.IGNORECASE)
            
            # remove bitrate type results
            # TODO
            # print(result)
            # recomp = re.compile(rf'^(?!{keyBitrateType})', flags=re.IGNORECASE)
            # print('-----', recomp.match(result[1]))
            # result = list(filter(lambda s: recomp.match, result))
            # print('b=', result)
            # del recomp
            print('out=', result)
            if result != []:
                result = result[0]
                result = re.findall(rf'\d+[ ,]?\d*[.,]?\d*(?= {keykbpsUnit}$)',
                                    result)[0]
                kbps.append(result)
            else:
                kbps.append('')
            
            # get track name
            result = re.findall(rf'^.*{keyTitle}.*$', metadata,
                                flags = re.MULTILINE | re.IGNORECASE)
            
            # get artist
            
            print(result)
    
    return bitrateType, kbps, title, artist
