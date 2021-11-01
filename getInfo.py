import sysFunctions
import fileFunctions

def getInfo(folderIn: str, folderOut: str) -> int:
    """
    Gets file info and writes it to a file.
    
    folderIn : str
        Folder being processed.
    
    folderOut: str
        Folder to which an output file is written.
    
    Returns None.
    """
    
    fileFunctions.pathChecks(folderIn)      # check "folderIn" correctness
    fileFunctions.pathChecks(folderOut)     # check "folderOut" correctness
    sysFunctions.limitTracebackInfo(0)      # limit traceback info
    fileInfoCmd = 'mediainfo'               # file info command
    sysFunctions.cmdInstalled(fileInfoCmd)  # check if command is installed
    fileFunctions.listFiles(folderIn, True) # list files in directory
    # write the structure to a file (rewrite existing or not)
    
    return 0

def test(path: str):
    import subprocess
    import os
    
    os.chdir(path)
    print(os.getcwd())
    res = subprocess.run(['mediainfo', 'test.mp3'], stdout=subprocess.PIPE)
    print(res.stdout.decode('utf-8'))

#test(r'/mnt/Internal_HDD/0_FROM_EXTERNAL/music/folder')
folder = r'/mnt/Internal_HDD/0_FROM_EXTERNAL/music/folder'
out = r'/home/linux/Documents'
getInfo(folder, out)
print('THE END')
