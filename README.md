# retroPiSaveSync
Keeps retro pi saves in sync with multiple devices. 

This will sync save files in google drive, including both .srm and .state filetypes.  If save file doesn't exist in gDrive, it will upload it with the file's timeUTC property as the description.  This property is then used to know whether or not to upload to google drive or download locally.

PyDrive will need to be installed, which can be found here: https://github.com/gsuitedevs/PyDrive 

This is best used on a schedule.  I have mine setup to sync hourly, or on reboot.
