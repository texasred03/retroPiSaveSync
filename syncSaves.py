#!/usr/bin/env python3
import os,glob
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def getUploadedSave(array, name):
  for x in array:
    if x["title"] == name:
        return x

def ListFolder(parent):
  filelist = []
  file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
  for f in file_list:
    filelist.append({"title":f['title'], "id":f['id'], "description":f['description']})
  return filelist

def isSaveNewer(uploadedUTC, localUTC):
  if localUTC > uploadedUTC:
    return 1
  elif uploadedUTC > localUTC:
    return -1
  return 0

def delSaveFile(id):
  delFile = drive.CreateFile({'id': id})
  delFile.Trash()
  
def uploadSaveFile(filePath, gameName, gameSystem, timeutc):
  uploadName = gameSystem + "_" + gameName
  print(uploadName + " uploading to gDrive.")
  saveFile = drive.CreateFile({'title': uploadName, 'description': timeutc, 'parents': [{'id': 'FOLDERID'}]})
  saveFile.SetContentFile(filePath)
  saveFile.Upload()

def downloadSaveFile(id, romsDir, gameName, gameSystem):
  savePath = romsDir + '/' + gameSystem + '/' + gameName + '.test'
  downloadFile = drive.CreateFile({'id': id})
  downloadFile.GetContentFile(savePath)
  print("Downloading " + gameName + " to " + savePath)

gauth = GoogleAuth()
# These next two lines are commneted out, only needed to create the creds
#gauth.CommandLineAuth() # client_secrets.json need to be in the same directory as the script
#gauth.SaveCredentialsFile("gDriveCreds.txt")
gauth.LoadCredentialsFile("gDriveCreds.txt")
drive = GoogleDrive(gauth)

save_folder_list = ListFolder('FOLDERID')
save_file_list = []
for saveFile in save_folder_list:
  save_file_list.append(saveFile['title'])

# Search /home/pi/RetroPie/roms/* for .srm and .state files
romsDir = "/home/pi/RetroPie/roms"
savesExt = ('.srm','.state')

for gameSystem in os.listdir(romsDir):
  for file in glob.glob(romsDir + "/" + gameSystem + "/*"):
    if file.endswith(savesExt):
      timeUTC = str(os.path.getmtime(file))
      gameName = file.split("/")[-1]
      uploadName = gameSystem + "_" + gameName

      if uploadName in save_file_list:
        uploadedSave = getUploadedSave(save_folder_list, uploadName)
        saveCompare = isSaveNewer(uploadedSave['description'],timeUTC)

        if(saveCompare > 0): # currentUTC > uploadedUTC, upload
          delSaveFile(uploadedSave['id'])
          uploadSaveFile(file, gameName, gameSystem, timeUTC)
        elif(saveCompare < 0): # currentUTC < uploadedUTC, download
          downloadSaveFile(uploadedSave['id'], romsDir, gameName, gameSystem)
      else: # save doesn't exist, upload
        uploadSaveFile(file, gameName, gameSystem, timeUTC)
