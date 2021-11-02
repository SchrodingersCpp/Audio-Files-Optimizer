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
    
    fileFunctions.dirCheck(folderIn)        # check "folderIn" correctness
    fileFunctions.dirCheck(folderOut)       # check "folderOut" correctness
    sysFunctions.limitTracebackInfo(0)      # limit traceback info
    fileName, fullName = \
        fileFunctions.listFiles(folderIn, True) # list files in directory
    fileFunctions.getMetadata(fullName)     # get metadata from filelist
    # write the structure to a file (rewrite existing or not)
    
    return 0

def test(path: str):
    import subprocess
    import os
    
    os.chdir(path)
    print(os.getcwd())
    res = subprocess.run(['mediainfo', '106 А.Миронов - Песня Остапа Бендера (12 стульев).mp3'], stdout=subprocess.PIPE)
    print(res.stdout.decode('utf-8'))

#test(r'/mnt/Internal_HDD/0_FROM_EXTERNAL/music/З_фільмів/12 стульев')
folder = r'/home/linux/Documents/TEST'
out = r'/home/linux/Documents'
print(getInfo(folder, out))
print('THE END')
