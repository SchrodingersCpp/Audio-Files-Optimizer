import sysFunctions
import typing
import os
import subprocess
import re
import csv
import datetime

def pathChecks(path: str) -> None:
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

def dirCheck(path: str) -> None:
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

def fileCheck(path: str) -> None:
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
            files.sort() # sort the files in a folder by name
            for file in files:
                fileName.append(file)
                fullName.append(os.path.join(root, file))
    else: # list files in the dir only
        files = os.listdir(path)
        files.sort() # sort the files in a folder by name
        for file in files:
            fullPath = os.path.join(path, file)
            if os.path.isfile(fullPath):
                fileName.append(file)
                fullName.append(fullPath)
    
    return fileName, fullName

def getMetadata(files: typing.List[str]) -> \
    typing.Tuple[typing.List[str], typing.List[str],
                 typing.List[str], typing.List[str]]:
    """
    Retrieve metadata from the list of files.
    
    files : List[str]
        List of files with their full paths.
    
    Returns:
        List of Bitrate Types : List[str].
        List of Bitrates (kbps) : List[str].
        List of song titles : List[str].
        List of song artists : List[str].
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
            print(f'{(str(nNP)+":").ljust(5)} "{file}" does not contain' +
                  ' an Audio Section!')
            
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
            recomp = re.compile(rf'^(?!{keyBitrateType})', flags=re.IGNORECASE)
            result = list(filter(recomp.match, result))
            del recomp
            
            if result != []:
                result = result[0]
                result = re.findall(rf'\d+[ ,]?\d*[.,]?\d*(?= {keykbpsUnit}$)',
                                    result)[0]
                result = result.replace(' ', '')
                kbps.append(result)
            else:
                kbps.append('')
            
            # get track name
            result = re.findall(rf'^{keyTitle} .*$', metadata,
                                flags = re.MULTILINE | re.IGNORECASE)
            if result != []:
                result = result[0]
                result = re.findall(r'(?<=: ).*$', result,
                                    flags = re.MULTILINE | re.IGNORECASE)[0]
                title.append(result)
            else:
                title.append('')
            
            # get artist
            result = re.findall(rf'^{keyArtist}.*$', metadata,
                                flags = re.MULTILINE | re.IGNORECASE)
            if result != []:
                result = result[0]
                result = re.findall(r'(?<=: ).*$', result,
                                    flags = re.MULTILINE | re.IGNORECASE)[0]
                artist.append(result)
            else:
                artist.append('')
    
    return bitrateType, kbps, title, artist

def getFileSize(files: typing.List[str]) -> typing.List[int]:
    """
    Get file size in bytes.
    
    files : List[str]
        List of files with their full paths.
    
    Returns:
        List of the file size in bytes : List[int].
    """
    
    sizeBytes = []
    for file in files:
        sizeBytes.append(os.stat(file).st_size)
    
    return sizeBytes

def getFileExtension(files: typing.List[str]) -> typing.List[str]:
    """
    Get file extensions.
    
    files : List[str]
        List of files with their full paths.
    
    Returns:
        List of the file extensions : List[str].
    """
    
    extensions = []
    for file in files:
        index = file.rfind('.') # search for the extension separator
        if index > -1: # if no file extension found
            ext = file[index+1:]
        else:
            ext = ''
        extensions.append(ext)
    
    return extensions

def writeData(rootFolder: str,
              fullNames: typing.List[str],
              fileNames: typing.List[str],
              extensions: typing.List[str],
              bitrateTypes: typing.List[str],
              kbps: typing.List[str],
              titles: typing.List[str],
              artists: typing.List[str],
              sizeBytes: typing.List[int],
              folderOut: str) -> None:
    """
    Write file data into a CSV file.
    
    rootFolder : str
        A root folder
    
    fullNames : List[str]
        List of files with their full paths.
    
    fileNames : List[str]
        List of file names.
    
    extensions : List[str]
        List of file extensions.
    
    bitrateTypes : List[str]
        List of Bitrate Types.
    
    kbps : List[str]
        List of Bitrates (kbps).
    
    titles : List[str]
        List of song titles.
    
    artists : List[str]
        List of song artists.
    
    sizeBytes : List[int]
        List of the file size in bytes.
    
    folderOut : str
        The folder to which save the output CSV file.
    
    Returns None.
    """
    
    timestamp = datetime.datetime.now() # get a timestamp for a filename
    outFileName = timestamp.strftime('out_%Y-%m-%d_%H-%M-%S.csv')
    
    # write data to the file
    with open(os.path.join(folderOut, outFileName), mode='w') as outcsv:
        writer = csv.writer(outcsv, dialect='excel')
        
        # write a header
        writer.writerow([f'Full Name ({rootFolder})', 'File Name', 'Extension',
                         'Bitrate Type', 'kb/s', 'Title', 'Artist',
                         'Size, bytes', 'File Name (new)', 'Title (new)',
                         'Artist (new)'])
        
        for i in range(len(fileNames)):
            row = [] # join info into a row
            row.append(fullNames[i])
            row.append(fileNames[i])
            row.append(extensions[i])
            row.append(bitrateTypes[i])
            row.append(kbps[i])
            row.append(titles[i])
            row.append(artists[i])
            row.append(sizeBytes[i])
            row.extend(['']*3)
            
            writer.writerow(row)
    
    return None
