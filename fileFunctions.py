import typing
import os

def pathChecks(path: str) -> bool:
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
    
    # check whether "path" is a folder
    if not os.path.isdir(path):
        raise Exception(f'Specified "path" ("{path}") is not a folder!')
    
    return None

def listFiles(path: str, recursive: bool = False) -> typing.List[str]:
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
