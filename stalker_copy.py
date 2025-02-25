import shutil

from os import sep
from os import path
from os import listdir
from os.path import isfile, join

mypath = r'C:\GAMMA\mods\New_posters\gamedata\meshes\dynamics\efp_props'

onlyfiles = [f for f in listdir(mypath)]

print(onlyfiles[0].rfind('.'))

poin = onlyfiles[0].rfind('.')

start_numb = int(onlyfiles[0][poin - 1])

n = 0

for i in range(21):
    n += 1
    
    shutil.copy(
        path.join(f'{mypath}', f'{onlyfiles[0]}'),
        path.join(f'{mypath}', f'{onlyfiles[0][0:poin - 1]}{start_numb + n}{onlyfiles[0][24:]}')
    )