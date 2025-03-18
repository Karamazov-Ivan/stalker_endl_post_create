import os
import shutil

from PIL import Image

se = os.sep


path = r'C:\GAMMA\mods\New_posters\gamedata\textures\item\not_text\Pictures\ALL_IMAGE'

path_horisontal = r'C:\GAMMA\mods\New_posters\gamedata\textures\item\not_text\Pictures\ALL_IMAGE\horisontal'

def recur_file_sieve(path, path_horisontal):

    for i in os.listdir(path):
        if i != 'horisontal':
            img = path + se + i
            if os.path.isdir(img):
                recur_file_sieve(img, path_horisontal)
            else:
                im = Image.open(img)
                width, height = im.size
                # print(width)
                if width > height:

                    shutil.copy(img, path_horisontal)
                    im.close()
                    os.remove(img)


recur_file_sieve(path, path_horisontal)
        

        # file_path = path + se + i
        # if os.isdir(file_path):
