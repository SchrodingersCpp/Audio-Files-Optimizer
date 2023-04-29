import fileFunctions as ff
import sysFunctions as sf

def getInfo(folderIn: str, folderOut: str) -> int:
    """
    Gets file info and writes it to a file.

    folderIn : str
        Folder being processed.

    folderOut: str
        Folder to which an output file is written.

    Returns 0.
    """

    sf.limitTracebackInfo(0) # limit traceback info
    ff.dirCheck(folderIn)    # check "folderIn" correctness
    ff.dirCheck(folderOut)   # check "folderOut" correctness

    fileName, fullName = ff.listFiles(folderIn, True) # list files in directory

    bitrateType, kbps, title, artist = \
        ff.getMetadata(fullName) # get metadata from filelist

    fileSize   = ff.getFileSize(fullName)      # get the size of the files
    extensions = ff.getFileExtension(fileName) # get files extensions

    ff.writeData(folderIn, fullName, fileName, extensions, bitrateType, kbps,
                 title, artist, fileSize, folderOut) # write data to a file

    return 0

if __name__ == '__main__':
    folder = r'/home/linux/Documents/TEST'
    out    = r'/home/linux/Documents/TESTOUT'
    print(getInfo(folder, out))

