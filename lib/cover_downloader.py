# Import External Libraries
from PIL import Image
from google_images_download import google_images_download

# Import System Libraries
from os import listdir, remove
from os.path import isfile, join


class CoverDownloader():
    def __init__(self):
        self.name = self.__class__.__name__

    def download(self, websearch, path='cache/cover_downloads/'):
        '''

        :param websearch:
        :param path:
        :return:
        '''
        clean_title = websearch.title.replace(':', '')
        keywords = '{0} Cover Poster'.format(clean_title)
        new_img = path + keywords + '/' + keywords + '.png'

        try:
            if not isfile(new_img):
                # Setting up Google Image Download
                google_downloader = google_images_download.googleimagesdownload()
                arguments = {"keywords": keywords, "limit": 1, 'output_directory': path}
                response = google_downloader.download(arguments)

                # Retrieving the downloaded image
                onlyfiles = [f for f in listdir(path + keywords + '/') if
                             isfile(join(path + keywords + '/', f))]
                original_img = path + keywords + '/' + onlyfiles[0]

                # Resizing the image for the poster box size
                img_temp = Image.open(original_img)
                img_temp = img_temp.resize((200, 272), Image.ANTIALIAS)

                # Save the resized file to the cache path
                img_temp.save(new_img, img_temp.format)

                # Clean up the original image from cache
                remove(original_img)
                return new_img

            print('File Already Exist, Skipping this Step - CoverDownloader')
            return new_img
        except Exception as err:
            print(self.name, ' ', err)
            return './interface/resources/placeholders/poster_placeholder.png'
