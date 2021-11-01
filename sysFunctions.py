def limitTracebackInfo(depth: int = 0) -> None:
    """
    Limits traceback information.
    
    depth : int
        Depth of traceback information output. Defaults to 0 (no output).
    
    Returns None.
    """
    
    # check "depth" argument type provided
    if not isinstance(depth, int):
        raise TypeError('"depth" must be an integer ' +
                        f'({type(depth)} was provided)!')
    
    # check "depth" argument value provided
    if depth < 0:
        raise ValueError('"depth" value must be positive or 0 ' +
                         f'("{depth}" was provided)!')
    
    # limit traceback information
    import sys
    sys.tracebacklimit = depth
    
    return None

def cmdInstalled(cmd: str) -> None:
    """
    Checks whether the specified command is installed.
    
    cmd : str
        Command to be checked.
    
    Returns None.
    """
    
    # check "cmd" argument type provided
    if not isinstance(cmd, str):
        raise TypeError('"cmd" must be a string ' +
                        f'("{type(cmd)}" was provided)!')
    
    # check whether cmd command is installed
    import shutil
    cmdInstalled = shutil.which(cmd)
    if cmdInstalled is None:
        raise Exception(f'"{cmd}" command is not installed!')
    
    return None