#!/usr/bin python

import os, os.path, time, urllib, mimetypes, csv, datetime, subprocess, base64, hashlib
from urllib.request import pathname2url

thumbnail = ["Thumbnail"]
fileNames = ["File Name"]
fileSize = ["File Size"]
imageMIME = ["MIME Type"]
lastModified = ["Last Modified"]
imageFilePaths = ["File Path"]

today = str(datetime.date.today())
backup_dir = input("directory to back up: ")
print(backup_dir)
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

for root, dirs, files in os.walk(backup_dir):
    print("hello")
    for imgFile in files:

        if imgFile.endswith((".tif")):

            originalFilePath = os.path.join(root, imgFile)
            print(root)
            rawSize = os.path.getsize(originalFilePath)
            easySize = humansize(rawSize)
            tiflessFilePath = originalFilePath.replace(".tif","")
            thumbPath = tiflessFilePath+".png"
            thumbHash = hashlib.sha1(originalFilePath.encode('utf-8')).hexdigest()
            thumbRenamedWithHashPath = thumbHash+".png"

            subprocess.call(['mogrify','-resize','300x300','-background','white','-gravity','center','-extent','300x300','-format','png',originalFilePath])
            subprocess.Popen(['mv',thumbPath,thumbRenamedWithHashPath])

            fileNames.append(imgFile)
            fileSize.append(easySize)
            imageFilePaths.append(originalFilePath)
            lastModified.append(time.ctime(os.path.getmtime(originalFilePath)))
            url = pathname2url(originalFilePath)
            imageMIME.append(mimetypes.guess_type(url)[0])
            
            try:
                thumbnail.append("<img src='../images/thumbs/"+thumbRenamedWithHashPath+"'>")
            except:
                encodedThumb = "COULDN'T THUMB"
                thumbnail.append(encodedThumb)

            subprocess.Popen(['mv', thumbRenamedWithHashPath, 'images/thumbs/'])

rows = zip(thumbnail,fileNames,fileSize,imageMIME,lastModified,imageFilePaths)
with open("/Users/michael/Desktop/cinefiles-backup-log_"+today+".csv", "w+")as bu:
    writer = csv.writer(bu, delimiter="\t")
    for row in rows:
        writer.writerow(row)