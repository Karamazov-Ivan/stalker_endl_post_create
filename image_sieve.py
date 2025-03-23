import os
import shutil

from PIL import Image

se = os.sep

path = r'' # Все картинки

path_horisontal = r'' # Папка для переноса горизонтальных картинок

def recur_file_sieve(path, path_horisontal):

    for i in os.listdir(path):
        if i != 'horisontal':
            img = path + se + i
            if os.path.isdir(img):
                recur_file_sieve(img, path_horisontal)
            else:
                im = Image.open(img)
                width, height = im.size
                if width > height:
                    im.close()
                    shutil.move(img, path_horisontal)


recur_file_sieve(path, path_horisontal)
