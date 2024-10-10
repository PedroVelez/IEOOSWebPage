import ftplib
import datetime
import os
import glob

## Read env data
HOME=os.environ['HOME']   
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='dirData' or Name=='dirAnalisis' or Name=='userFTP' or Name=='passwdFTP':
        exec(Name + "=" + "'" + Content + "'")
f.close()

imagesDir = dirAnalisis + '/IEOOSWebPage/images'

os.chdir(imagesDir)

## Demarcaciones
session = ftplib.FTP('ftp.oceanografia.es',userFTP,passwdFTP)
session.cwd('/html/IEOOS/reanalisis/images')

filenames = glob.glob(imagesDir+'/*.png')
for filename in filenames:
    print('https://www.oceanografia.es/IEOOS/reanalisis/images/'+filename.split('/')[-1])
    session.storbinary('STOR '+ filename.split('/')[-1], open(filename, 'rb'))

session.quit()    
