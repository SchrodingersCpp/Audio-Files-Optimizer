import typing

def pathChecks(path: str) -> bool:
    """
    Performs correctness checks for the specified path.
    
    path : str
        Path to the specified folder.
    
    Returns None.
    """
    
    import os
    
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
    
    Returns a list of full path to the files : List[str].
    """
    
    # check "recursive" argument type provided
    if not isinstance(recursive, bool):
        raise TypeError('"recursive" must be a boolean ' +
                        f'("{type(recursive)}" was provided)!')
    
    
    