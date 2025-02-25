import pyautogui as pau
import win32clipboard
import os
import time


result_mes_path = r'C:\GAMMA\mods\New_posters\gamedata\meshes\dynamics\efp_props'

# mouseX, mouseY = pau.position()

# 'item\posters\3\poster3_1'
# 'item\posters\3\poster10_1
# texture_path = r'item\posters\3\poster'

def clip_copy_boart(copy_text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(copy_text)
    win32clipboard.CloseClipboard()

def clip_pate_board():
    # get clipboard data
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()


# prop_poster_vertical_3_1


# pau.ho

cou = 1

file_numb = 1

l_dir_work = os.listdir(result_mes_path)

all_num = len(l_dir_work)

for i in l_dir_work:
    str_time = time.time()
    print(f'{file_numb}/{all_num}')
    file_numb += 1
    start_txt = i.rfind('l')
    fin_lower = i.rfind('_')
    fin_txt = i.rfind('.')
    # item\posters\3\poster3_1
    # prop_poster_vertical_7_65
    # print(rf'item\posters\{i[start_txt + 2:fin_lower]}\poster' + i[start_txt + 2:fin_txt])
    # exit()
    clip_copy_boart(rf'item\posters\{i[start_txt + 2:fin_lower]}\poster' + i[start_txt + 2:fin_txt])
    
    os.startfile(result_mes_path + os.sep + i)
    time.sleep(0.5)

    pau.moveTo(x=852, y=443)

    if cou == 1:
        time.sleep(0.1)

    cou = 0

    pau.click()
    
    pau.hotkey('ctrl', 'a')
    # time.sleep(0.1)
    
    pau.hotkey('ctrl', 'v')
    # time.sleep(0.1)
    pau.hotkey('ctrl', 's')
    time.sleep(0.1)
    pau.press('enter')
    time.sleep(0.1)

    pau.hotkey('alt', 'f4')
    time.sleep(0.1)
    fin_time = time.time()
    print(f'{round(avg_t := (fin_time - str_time), 4)} sec.  Approximately time left: {round(((all_num - file_numb) * avg_t) / 60, 4)} min.')
