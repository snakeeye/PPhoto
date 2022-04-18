#!/usr/bin/python3
from fileinput import filename
from operator import contains
import os
import sys
import argparse
import os
import time
import datetime
import hashlib


globTargetFolder=""
globDryRun=True
def parseFile(folderPath, fileName):
    if fileName == ".DS_Store":
        return

    sourceFilePath = folderPath + "/" + fileName

    # check source file exist
    if os.path.isfile(sourceFilePath) == False:
        print ("SourceFile is not exist:" + sourceFilePath)
        return

    # only parse image file and movie file
    if isImageFile(sourceFilePath) == False and isMovieFile(sourceFilePath) == False:
        print ("File is not image and movie file, skip " + sourceFilePath);
        return

    fileDate = getFileDate(sourceFilePath)

    fileMonth = fileDate.month;
    fileMonthStr = "%02d" % fileMonth
    targetFolder = globTargetFolder + "/" + repr(fileDate.year) + "/" + fileMonthStr + "/"
    targetFilePath =  targetFolder + fileName

    dupTargetFolder = targetFolder + "dup/"
    dupSourceFolder = folderPath   + "/dup/"

    print (sourceFilePath + "-->" + targetFilePath)
    if globDryRun:
        return
    
    ensureFolder(targetFolder)

    if os.path.isfile(targetFilePath) == False: #Target File not exist
        os.rename(sourceFilePath, targetFilePath)
    else:
        if (isFileMD5Same(sourceFilePath, targetFilePath) == False):
            if os.path.isfile(dupTargetFolder + fileName) == False:
                print ("Same Name exist, but different file, prefix with dup：" + dupTargetFolder + fileName)
                ensureFolder(dupTargetFolder)
                os.rename(sourceFilePath,  dupTargetFolder + fileName)
                
        else:
            if os.path.isfile(dupSourceFolder + fileName) == False:
                print ("Same file exist, move to duplicate folder:" + dupSourceFolder + fileName)
                ensureFolder(dupSourceFolder)
                os.rename(sourceFilePath, dupSourceFolder + fileName)
                
    return

def ensureFolder(folder):
    if os.path.exists(folder) != True:
        os.makedirs (folder)


def getFileDate(filePath):
    fileDate = datetime.date(1990,1,1) # default value 1990-01-01
    try:
        fileDate = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))
    except:
        print ("Fail GetDate" + filePath)   
        pass
    
    # if (isImageFile(filePath)):
    #     fileDate = getImageExifCreationDate(filePath)

    return fileDate


def isImageFile(filePath):
    fileName = os.path.basename(filePath)
    fileExt = os.path.splitext(fileName)[1]
    if fileExt == ".jpg" or fileExt == ".JPG" or fileExt == ".jpeg" or fileExt == ".JPEG" or fileExt == ".HEIC" or fileExt == ".heic" or fileExt == ".png" or fileExt == ".PNG" or fileExt == ".gif" or fileExt == ".GIF" or fileExt == ".CR2" or fileExt == ".cr2" or fileExt == ".TIF" or fileExt == ".tif":
        return True
    return False

# def getImageExifCreationDate(filePath):
#     pass

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def isFileMD5Same(filePath1, filePath2):
    file1Hash = md5(filePath1)
    file2Hash = md5(filePath2)
    return file1Hash == file2Hash

def isMovieFile(filePath):
    fileName = os.path.basename(filePath)
    fileExt = os.path.splitext(fileName)[1]
    if fileExt == ".mov" or fileExt == ".MOV" or fileExt == ".MP4" or fileExt == ".mp4" or fileExt == ".MPG" or fileExt == ".mpg":
        return True
    return False

def parseFolder(folder):
    for root, dirs, files in os.walk(folder):
        print (root)
        if "dup" in root:
            print ("Skip Duplicate Folder:" + root)
            continue

        for file in files:
            parseFile(root, file)
    return

def main():
    args = parseArgs()
    sourceFolder = args["source"]
    global globTargetFolder
    globTargetFolder = args["target"]
    global globDryRun
    globDryRun = args["dryrun"]
    print ("SourceFolder="+sourceFolder)
    print ("TargetFolder="+globTargetFolder)
    parseFolder(sourceFolder)

def parseArgs():
    parser = argparse.ArgumentParser(description="Photo Export")
    parser.add_argument("-s", "--source", required=True, help="Source Photo Folder")
    parser.add_argument("-t", "--target", required=True, help="Target Photo Folder, Will create it not exist")
    parser.add_argument("-d", "--dryrun", required=False, action='store_false', default=False, help="Show command string only")
    return vars(parser.parse_args())

if __name__ == "__main__":
    main()
