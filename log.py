#!/usr/bin python

import os, os.path, time, urllib, mimetypes, csv, datetime, subprocess, base64, hashlib, mmap, re
from urllib.request import pathname2url

thumbnail = ["Thumbnail"]
fileNames = ["File Name"]
fileSize = ["File Size"]
imageMIME = ["MIME Type"]
lastModified = ["Last Modified"]
imageFilePaths = ["File Path"]
imageHash = ["Hash of original image path"]

today = str(datetime.date.today())
backup_dir = ("/Volumes/DroboFW/cinefiles-backed-up/")

with open("lastLoggedOn.txt", "r") as last:
    lastLoggedOn = last.readlines()
    lastLoggedOn = lastLoggedOn[0]
    print(lastLoggedOn)

# this file size calc came from:
# http://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

with open("hashList.txt","r") as hashes:
    hashMap = mmap.mmap(hashes.fileno(), 0, access=mmap.ACCESS_READ)


#### CREATE A MEMORY MAP OF THE HASH LIST TO SEE IF THE GIVEN FILE HAS BEEN LOGGED ALREADY
#### IF IT HASN'T BEEN LOGGED, THE PROCESS WILL ADD THE HASH TO THE LIST

def checkHash(thumbHash):
    byteHash = thumbHash.encode()

    with open("hashList.txt","a+") as hashList:

        if hashMap.find(byteHash) != -1:
            return True  
        else:
            hashList.write(thumbHash+"\r")

fileRegexPattern = re.compile(r".*tif")

for root, dirs, files in os.walk(backup_dir):

    for imgFile in files:
        if fileRegexPattern.match(imgFile):

            originalFilePath = os.path.join(root, imgFile)
            url = pathname2url(originalFilePath)

            rawSize = os.path.getsize(originalFilePath)
            easySize = humansize(rawSize)
            
            #### CREATE PNG FILEPATH, HASH ORIGINAL FILEPATH AND CREATE THE NEW FILENAME WITH IT

            tiflessFilePath = originalFilePath.replace(".tif","")
            thumbPath = tiflessFilePath+".png"
            thumbHash = hashlib.sha1(originalFilePath.encode('utf-8')).hexdigest()
            thumbRenamedWithHashPath = thumbHash+".png"

            #### CHECK IF THE FILE HAS BEEN LOGGED ALREADY

            status = checkHash(thumbHash)
            print(status)

            if not status:

                #### CREATE PNG THUMBNAIL AND RENAME IT WITH THE HASH OF THE ORIGINAL FILEPATH

                subprocess.call(['mogrify','-resize','300x300','-background','white','-gravity','center','-extent','300x300','-format','png',originalFilePath])
                subprocess.call(['mv',thumbPath,thumbRenamedWithHashPath])

                #### WRITE OUTPUT TO TEMPORARY LISTS

                fileNames.append(imgFile)
                fileSize.append(easySize)
                imageFilePaths.append(originalFilePath)
                lastModified.append(time.ctime(os.path.getmtime(originalFilePath)))
                imageMIME.append(mimetypes.guess_type(url)[0])
                imageHash.append(thumbHash)
                
                #### IF THE THUMBNAIL PROCESS DIDN'T WORK, MAKE A NOTE OF IT

                try:
                    thumbnail.append("<img src='../images/thumbs/"+thumbRenamedWithHashPath+"'>")
                except:
                    thumb = "COULDN'T THUMB"
                    thumbnail.append(thumb)

                #### MOVE THE FINAL THUMBNAIL INTO THE IMAGES/THUMBS/ DIRECTORY

                try:
                    subprocess.Popen(['mv', thumbRenamedWithHashPath, 'images/thumbs/'])
                except:
                    print("move didn't work"+("&")*100)
            elif status == True:
                print(checkHash(thumbHash))
                print(imgFile+" already logged... moving on...")
            else:
                print("something else is going on")

rows = zip(thumbnail,fileNames,fileSize,imageMIME,lastModified,imageFilePaths,imageHash)


with open("data/cinefiles-backup-log_"+today+".csv", "w+")as bu:
    writer = csv.writer(bu, delimiter="\t")
    for row in rows:
        writer.writerow(row)

def updateInputCSV(lastDate, today):
    with open("index.html", "r") as main:
        content = main.read()
        if lastDate in content:
            newContent = content.replace(lastDate, today)
            return newContent

#### UPDATE INDEX.HTML WITH THE CURRENT CSV LOG

with open("index.html", "r+") as index: 
    new = updateInputCSV(lastLoggedOn, today)
    index.write(new)

with open("lastLoggedOn.txt", "w+") as last:
    last.write(today)