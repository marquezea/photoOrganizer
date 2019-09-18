import os
import shutil
import datetime
from PIL import Image

class PhotoOrganizer:
    extensions = ['jpg','jpeg','png','JPG','JPEG','PNG']

    def getFolderPathFromPhotoDate(self, file):
        date = self.getPhotoShootingDate(file)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m-%d')


    def getPhotoShootingDate(self, file):
        photo = Image.open(file)
        info = photo._getexif()
        if (info == None):
            date = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        else:
            if 36867 in info:
                date = info[36867]
                date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
            else:
                date = datetime.datetime.fromtimestamp(os.path.getmtime(file))

        return date

    def movePhoto(self, file):
        new_folder = self.getFolderPathFromPhotoDate(file)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        print(new_folder + '/' + file)
        shutil.move(file, new_folder + '/' + file)

    def organize(self):
        photos = [
            filename for filename in os.listdir('.') if any(filename.endswith(ext) for ext in self.extensions)
        ]
        for filename in photos:
            self.movePhoto(filename)

PO = PhotoOrganizer()
PO.organize()