import os
import time
import shutil
import win32clipboard
import sqlite3 as sl
import pyautogui as pau
import mod_fold.poster_item_templ as m_itm
import mod_fold.poster_sql_db as m_db
import mod_fold.poster_loot_quality as m_ql
import mod_fold.poster_identif as m_pi
# import re
# import win32gui

from sys import stdout
# from os import path
# from os import listdir
# from os import sep
# from os.path import isfile, join

#Копирование мешей ----------------------------------------------------------------------------------------------

def main():

    se = os.sep

    texture_list = []

    connection = sl.connect('textures.db')

    poster_item_name = 'decor_poster' # Наименование постера в items

    gamma_main_path = r'C:\GAMMA\mods\New_posters\gamedata'

    path = gamma_main_path + se + r'textures\item\posters' # Текустуры постеров
    post_new_file = gamma_main_path + se + r'configs\items\items\items_new_posters_pos.ltx'

    # ref_mesh_path = r'D:\Python\projects\stalker' # Референс вертикального постера
    ref_mesh_path = os.getcwd() # Референс вертикального постера
    ref_mesh_file = 'poster_refer_mesh.ogf'
    result_mes_path = gamma_main_path + se + r'meshes\dynamics\efp_props' # Меши постеров
    mesh_ful_file_path = ref_mesh_path + os.sep + ref_mesh_file
    ref_mesh_horizon_file = 'poster_refer_mesh_horizont.ogf'
    mesh_horizon_ful_file_path = ref_mesh_path + os.sep + ref_mesh_horizon_file

    post_content_new_file = gamma_main_path + se + r'configs\items\settings\itms_manager_posters.ltx' # Содержимое журнала (лутбокс)

    post_parts_new_file = gamma_main_path + se + r'configs\items\settings\mod_parts_posters_3.ltx' # Части постеров и журналов для разборки (бумага)
    poster_mesh_path = gamma_main_path + se + r'meshes\dynamics\equipments\trade' # Меши журналов

    description_rus_path = gamma_main_path + se + r'configs\text\rus' # Описание айтемов, русский язык

    wg_texture_descr_path =  gamma_main_path + se + r'configs\ui\textures_descr' # Описание читаемых текстур для WG xml

    def print_slow(str_1):
        for letter in (str_1.split(' ')):
            stdout.write(letter + ' ')
            stdout.flush()
            time.sleep(0.01)

    def rename_files(res_list):
        'Переименовывает все текстуры в папках'
        err = 0
        file_numb = 0
        for folder in os.listdir(path):
            basic_folder = path + se + folder
            if os.path.isdir(basic_folder):
                for rare_folder in os.listdir(basic_folder):
                    if os.path.isdir(basic_folder + se + rare_folder):
                        for picture in os.listdir(basic_folder + se + rare_folder):
                            file_numb += 1
                            if picture.endswith('.dds'):
                                old_name = basic_folder + se + rare_folder + se + picture
                                tex_name = f'poster{folder}_{rare_folder}_{file_numb:04}'
                                new_name = f'{basic_folder + se + rare_folder + se}{tex_name}.dds'
                                
                                res_list.append((tex_name, basic_folder + se + rare_folder + se + tex_name))
                                try:
                                    os.rename(old_name, new_name)
                                except Exception as e:
                                    err += 1
                                    # print(e)
        print('Текстуры переименованы')
        print(f'Exceptiosns rename .dds count: {err}')

    def create_poster_items(connec):
        'Записывает новые айтемы постеров'
        
        tex_item_coun = 0
        sql = m_db.SqlTextureDB()
        with open(post_new_file, 'w') as f:
            for texture_name in sql.select_from(con=connec, query_num=2):
                print(texture_name[0][6:])
                tex_item_coun += 1
                rarity_id = texture_name[0][9:10]
                f.write(m_itm.text_post(texture_name[0][6:], cost=m_pi.rarity_identif(rarity_id)[1]))
                f.write('\n\n')
        print(f'Айтемы постеров созданы: {tex_item_coun} шт.')

    def copy_poster_mesh(connec, del_mesh=0):
        'Копирует меши и удаляет(опционально)'
        
        mes_coun = 0
        if del_mesh == 1:
            for file in os.listdir(result_mes_path):
                os.remove(result_mes_path + se + file)

        sql = m_db.SqlTextureDB()            
        for texture_name in sql.select_from(con=connec, query_num=1):
            if texture_name[0][9] == '7':
                mes_coun += 1
                shutil.copy(mesh_horizon_ful_file_path, result_mes_path + os.sep + f'prop_poster_vertical_{texture_name[0][6:]}.ogf')
            else:
                mes_coun += 1
                shutil.copy(mesh_ful_file_path, result_mes_path + os.sep + f'prop_poster_vertical_{texture_name[0][6:]}.ogf')
        print(f'Меши постеров созданы: {mes_coun}, предыдущие копии удалены')

    def create_lootbox_content(connec):
        'Записывает содержимое (журналов)лутбоксов'

        sql = m_db.SqlTextureDB()

        with open(post_content_new_file, 'w') as pst_cont:

            for rare_name in m_ql.loot_quality_list:
                pst_cont.write(f'[{rare_name}]')
                pst_cont.write('\n')                
                
                for mag in os.listdir(poster_mesh_path):
                    mag_numb = mag[11:13]

                    sql_rar_mag_code = f'''
                        SELECT name
                        FROM (
                            SELECT
                                name
                                ,SUBSTRING(name, 7, 2) AS mag
                                ,SUBSTRING(name, 10, 1) AS rare
                                ,SUBSTRING(name, 12, 4) AS numb
                            FROM TEXTURE_TABLE
                        ) AS result_t
                        WHERE mag = '{mag_numb}' AND rare = '{m_ql.loot_quality_dict[rare_name]}'
                    '''

                    sql_rar_mag_name = sql.select_from(con=connec, direct_quer=sql_rar_mag_code)
                    
                    pst_cont.write(f'new_mag_pos{mag_numb} = ' + ','.join(['decor_' + r[0] for r in sql_rar_mag_name]))
                    pst_cont.write('\n')
                pst_cont.write('\n')
        print('Содержимое журналов(лутбокс) записано')

    def create_items_parts_paper():
        'Добавляет журналу/постеру часть Бумага 1шт. для разборки (Меши должны быть)'
        
        with open(post_parts_new_file, 'w') as prts_file:
            prts_file.write('![nor_parts_list]\n')
            # Ищет все журналы по мешам в папке
            for mag_mesh in os.listdir(poster_mesh_path):
                mag_nub = mag_mesh[mag_mesh.rfind('s') + 1:mag_mesh.rfind('.')]
                prts_file.write(f'new_mag_pos{mag_nub} = prt_i_paper\n')
            
            # Ищет все посетеры по мешам в папке
            for post_mesh in os.listdir(result_mes_path):
                post_num = post_mesh[post_mesh.rfind('l') + 2:post_mesh.rfind('.')]
                prts_file.write(f'{poster_item_name}{post_num} = prt_i_paper\n')
        print('Части журналов, плакатов записаны (бумага)')
    
    def create_rare_folders():
        # ('1-basic', '2-uncommon', '3-rare', '4-epic', '5-legend', '6-new_year', '7-spec')
        dir_tuple = ('1', '2', '3', '4', '5', '6', '7')
        for folder_name in os.listdir(path):
            for rare_name in dir_tuple:
                os.mkdir(path + os.sep + folder_name + os.sep + rare_name)

    def poster_item_descr(num, rarity_id, descript, poster_name):
        
        rar = m_pi.rarity_identif(rarity_id)[0]
        poster_item_descr_text = rf'''
    <string id="st_placeable_poster{num}">
        <text>{poster_name}</text>
    </string>
    <string id="st_placeable_poster{num}_descr">
        <text>%c[ui_gray_2]{descript}{num[-4:]}\n \n
        %c[0,255,255,255]РЕДКОСТЬ ВЫПУСКА: {rar}\n
        %c[ui_gray_2]ХАРАКТЕРИСТИКИ:\n
        %c[d_cyan] • %c[pda_white] Размещаемое\n
        </text>
    </string>'''
        return poster_item_descr_text
    
    def poster_texture_descr_wg(connec):
        
        sql = m_db.SqlTextureDB()
        
        def tex_desc_template_def(some_tex_path, some_texture_name):

            tex_desc_template = f"""
    <file name="{some_tex_path}.dds">
        <texture id="ui_decor_poster{some_texture_name}_page_1"               x="0"    y="0"    width="2048"    height="1024"/>
    </file>"""
            return tex_desc_template

        with open(wg_texture_descr_path + se + 'ui_rick_magazine.xml', 'w') as xml_desc2:
            xml_desc2.write('<w>')
            # xml_desc2.write('\n')

            dir_quer = 'SELECT path, name FROM TEXTURE_TABLE'


            for texture_name in sql.select_from(con=connec, direct_quer=dir_quer): 
                xml_desc2.write(tex_desc_template_def(texture_name[0][-33:], texture_name[1][-9:]))
                xml_desc2.write('\n')
            xml_desc2.write('</w>')

        print('Описание постеров записано')       

        
        

    def create_description_xml(connec):

        sql = m_db.SqlTextureDB()
            
        with open(description_rus_path + se + 'poster_descrip.xml', 'w') as xml_desc:
            xml_desc.write('<?xml version="1.0" encoding="windows-1251"?>')
            xml_desc.write('\n\n')
            xml_desc.write('<string_table>\n')
            for texture_name in sql.select_from(con=connec, query_num=2):
                mag_id = texture_name[0][6:8]
                desc_name = m_pi.descrip_identif(mag_id)
                xml_desc.write(poster_item_descr(num=texture_name[0][6:], rarity_id=texture_name[0][9:10], descript=desc_name[0], poster_name=desc_name[1])) #, encoding='WINDOWS-1251', xml_declaration=True)
                xml_desc.write('\n')
            xml_desc.write('</string_table>')
        print('Описание постеров записано')

    def clip_copy_boart(copy_text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(copy_text)
        win32clipboard.CloseClipboard()

    # def clip_pate_board():
    #     # get clipboard data
    #     win32clipboard.OpenClipboard()
    #     data = win32clipboard.GetClipboardData()
    #     win32clipboard.CloseClipboard()

    def way_writer(connec):

        l_dir_work = os.listdir(result_mes_path)
        all_num = len(l_dir_work)
        file_numb = 1
        sql = m_db.SqlTextureDB()
        dir_quer = 'SELECT name, path FROM TEXTURE_TABLE'
        textures_lis =  sql.select_from(con=connec, direct_quer=dir_quer)
        mesh_lis = os.listdir(result_mes_path)
        for mesh in mesh_lis:
            print(f'{file_numb}/{all_num}')
            file_numb += 1
            str_time = time.time()
            for texture in textures_lis:
                if mesh.endswith(f'{texture[0][-9:]}.ogf'):
                    clip_copy_boart(texture[1][-33:])
                    os.startfile(result_mes_path + os.sep + mesh)
                    time.sleep(0.5)

                    pau.moveTo(x=852, y=443)

                    time.sleep(0.1)

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

    def menu_func():
        while True:
            # print_slow('''
            print('''
            Меню:\n
            1. Пересоздать БД с текстурами
            2. Переименовать текстуры постеров и внести в БД
            3. SELECT * БД
            4. Создать айтемы для постеров
            5. Создать меши для текстур постеров
            6. Создать содержимое журналов(лутбоксы)
            7. Создать содержимое журналов и плакатов (бумага)
            8. Создать описание для постеров
            9. Указать пути для текстур мешей
            10. Создать описание текступ для Western Goods
            0. Выход
            ''')
            try:
                inp = int(input('\nВвод: '))
            except:
                inp = 100
            sql_class = m_db.SqlTextureDB()

            if inp == 1:
                sql_class.create_tab(connection)
                input()
            elif inp == 2:
                sql_class.delete_from(connection)
                input()
                rename_files(texture_list)
                input()
                sql_class.insert_data(connection, texture_list)
                input()
            elif inp == 3:
                num = 0
                for i in sql_class.select_from(connection):
                    num += 1
                    print(f'{num}. {i}')
                input()
            elif inp == 4:
                create_poster_items(connec=connection)
                input()
            elif inp == 5:
                inp_2 = input('Данное действие перезапишет все меши, продолжить? (д/н)')
                if inp_2 in ('д', 'y'):
                    copy_poster_mesh(connec=connection, del_mesh=1)
                else:
                    print('Ничего')
                input()
            elif inp == 6:
                create_lootbox_content(connec=connection)
                input()
            elif inp == 7:
                create_items_parts_paper()
                input()
            elif inp == 8:
                create_description_xml(connec=connection)
                input()
            elif inp == 9:
                way_writer(connec=connection)
                input()
            elif inp == 10:
                poster_texture_descr_wg(connec=connection)
                input()
            elif inp == 0:
                break
            else:
                print('Ошибка, команда не найдена')
                input()
    
    menu_func()

if __name__ == '__main__':
        main()
    # try:
    # except Exception as err:
    #     print(err)

