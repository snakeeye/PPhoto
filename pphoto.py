#!/usr/bin/python
import os
import sys
import argparse
import os
import time
import datetime

globTargetFolder=""
globDryRun=False
def parseFile(folderPath, fileName):
    if fileName == ".DS_Store":
        return

    sourceFilePath = folderPath + "/" + fileName
    try:
        fileDate = datetime.datetime.fromtimestamp(os.path.getctime(sourceFilePath))
    except:
        print "Fail GetDate" + sourceFilePath
        return

    fileMonth = fileDate.month;
    fileMonthStr = "%02d" % fileMonth
    targetFolder = globTargetFolder + "/" + repr(fileDate.year) + "/" + fileMonthStr + "/"
    targetFilePath =  targetFolder + fileName

    print sourceFilePath + "-->" + targetFilePath
    if globDryRun:
        return

    if os.path.exists(targetFolder) != True:
        os.makedirs (targetFolder)

    if os.path.isfile(sourceFilePath) == False:
        print "SourceFile Not Exist" + sourceFilePath
        return

    if os.path.isfile(targetFilePath) == False: #Target File not exist
        os.rename(sourceFilePath, targetFilePath)
    else:
        print "TargetFile Exist" + targetFilePath
    return

def parseFolder(folder):
    for root, dirs, files in os.walk(folder):
        print root
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
    print "SourceFolder="+sourceFolder
    print "TargetFolder="+globTargetFolder
    parseFolder(sourceFolder)

def parseArgs():
    parser = argparse.ArgumentParser(description="Photo Export")
    parser.add_argument("-s", "--source", required=True, help="Source Photo Folder")
    parser.add_argument("-t", "--target", required=True, help="Target Photo Folder, Will create it not exist")
    parser.add_argument("-d", "--dryrun", required=False, action='store_false', default=False, help="Show command string only")
    return vars(parser.parse_args())

if __name__ == "__main__":
    main()
