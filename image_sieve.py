import os
import shutil

from PIL import Image

se = os.sep


path = r'C:\GAMMA\mods\New_posters\gamedata\textures\item\not_text\photo_packet'

path_horisontal = r'C:\GAMMA\mods\New_posters\gamedata\textures\item\not_text\photo_packet_hor'



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
                    im.close()
                    shutil.move(img, path_horisontal)
                    # shutil.copy(img, path_horisontal)
                    # os.remove(img)


# def recur_file_sieve_square(path, path_horisontal_may):

#     for i in os.listdir(path):
#         if i not in ('horisontal_may', 'horisontal'):
#             img = path + se + i
#             if os.path.isdir(img):
#                 recur_file_sieve_square(img, path_horisontal_may)
#             else:
#                 im = Image.open(img)
#                 width, height = im.size
#                 # print(width)
#                 if (height / width) < 1.15:
#                     try:
#                         shutil.move(img, path_horisontal_may)
#                         im.close()
#                         os.remove(img)
#                     except Exception as e:
#                         print(e)
#                         if str(e).startswith(r"Destination path"):
#                             # print(1)
#                             im.close()
#                             os.remove(img)




recur_file_sieve(path, path_horisontal)

# recur_file_sieve_square(path, path_horisontal_may)
        

        # file_path = path + se + i
        # if os.isdir(file_path):
