from google_images_download import google_images_download
from os import listdir
from os.path import isfile, join
from PIL import Image

class CoverDownloader():
    def __init__(self):
        self.name = self.__class__.__name__

    def download(self, websearch):
        response = google_images_download.googleimagesdownload()

        keywords = '{0} cover poster'.format(websearch.title)

        arguments = {"keywords": '{0} cover poster'.format(websearch.title), "limit": 1}
        d = response.download(arguments)
        onlyfiles = [f for f in listdir('./downloads/' + keywords + '/') if
                     isfile(join('./downloads/' + keywords + '/', f))]

        img_temp = Image.open('./downloads/' + keywords + '/' + onlyfiles[0])
        img_temp = img_temp.resize((200, 272), Image.ANTIALIAS)
        img_temp.save(('./downloads/' + keywords + '/' + '{0}-Poster-Cover.png'.format(websearch.title)), img_temp.format)
        return ('./downloads/' + keywords + '/' + '{0}-Poster-Cover.png'.format(websearch.title))

