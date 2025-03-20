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
import configparser
# import win32gui

from PIL import Image
from sys import stdout
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
# from os import path
# from os import listdir
# from os import sep
# from os.path import isfile, join

def main():

    se = os.sep
    ref_mesh_path = os.getcwd()
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("config.ini")  # читаем конфиг

    # Переменные из конфига
    gamma_main_path = config["settings"]["gamma_main_path"].encode('unicode_escape').decode()
    poster_item_name = config["settings"]["poster_item_name"]
    ref_mesh_file = config["settings"]["ref_mesh_file"]
    ref_mesh_horizon_file = config["settings"]["ref_mesh_horizon_file"]

    texture_list = []
    connection = sl.connect('textures.db')

    gamma_main_path = r'C:\GAMMA\mods\New_posters\gamedata'
    poster_item_name = 'decor_poster' # Наименование постера в items
    ref_mesh_file = 'poster_refer_mesh.ogf'
    ref_mesh_horizon_file = 'poster_refer_mesh_horizont.ogf'

    mesh_ful_file_path = ref_mesh_path + os.sep + ref_mesh_file # Референс вертикального постера
    mesh_horizon_ful_file_path = ref_mesh_path + os.sep + ref_mesh_horizon_file # Референс горизонтального постера
    path = gamma_main_path + se + r'textures\item\posters' # Текустуры постеров
    post_new_file = gamma_main_path + se + r'configs\items\items\items_new_posters_pos.ltx' # Айтемы постеров
    result_mes_path = gamma_main_path + se + r'meshes\dynamics\efp_props' # Меши постеров в gamedata
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
            sql_que = 'SELECT name, path FROM TEXTURE_TABLE'
            for texture_name in sql.select_from(con=connec, direct_quer=sql_que):
                im = Image.open(f'{texture_name[1]}.dds')
                width, height = im.size
                if height == 2048:
                    tex_item_coun += 1
                    rarity_id = texture_name[0][9:10]
                    f.write(m_itm.text_post_horizont(texture_name[0][6:], cost=m_pi.rarity_identif(rarity_id)[1]))
                    f.write('\n\n')
                else:
                    tex_item_coun += 1
                    rarity_id = texture_name[0][9:10]
                    f.write(m_itm.text_post(texture_name[0][6:], cost=m_pi.rarity_identif(rarity_id)[1]))
                    f.write('\n\n')
        print(f'Айтемы постеров записаны: {tex_item_coun} шт.')

    def copy_poster_mesh(connec, del_mesh=0):
        'Копирует меши и удаляет(опционально)'
        
        mes_coun = 0
        if del_mesh == 1:
            for file in os.listdir(result_mes_path):
                os.remove(result_mes_path + se + file)

        sql = m_db.SqlTextureDB()            
        for texture_name in sql.select_from(con=connec, query_num=1):
            im = Image.open(f'{texture_name[4]}.dds')
            width, height = im.size
            if texture_name[0][9] == '7' or height == 2048:
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
    
    def create_rare_folders(dir_count):
        'Доп функция. Создаёт папки с id редкости для разметки'

        # ('1-basic', '2-uncommon', '3-rare', '4-epic', '5-legend', '6-new_year', '7-spec')
        dir_tuple = ('1', '2', '3', '4', '5', '6', '7')
        # range(dir_count)
        for folder_name in os.listdir(path):
            for rare_name in dir_tuple:
                os.mkdir(path + os.sep + folder_name + os.sep + rare_name)

    def poster_item_descr(num, rarity_id, descript, poster_name, post_numb):
        rar = m_pi.rarity_identif(rarity_id)[0]
        poster_item_descr_text = rf'''
    <string id="st_placeable_poster{num}">
        <text>{poster_name} #{post_numb}</text>
    </string>
    <string id="st_placeable_poster{num}_descr">
        <text>%c[ui_gray_2]{descript}{post_numb}\n \n
        %c[0,255,255,255]РЕДКОСТЬ ВЫПУСКА: {rar}\n
        %c[ui_gray_2]ХАРАКТЕРИСТИКИ:\n
        %c[d_cyan] • %c[pda_white] Размещаемое\n
        </text>
    </string>'''
        return poster_item_descr_text
    
    def poster_texture_descr_wg(connec):
        'Создать описание текступ для Western Goods'
        
        sql = m_db.SqlTextureDB()
        
        def tex_desc_template_def(some_tex_path, some_texture_name, w=2048, h=1024):

            tex_desc_template = f"""
    <file name="{some_tex_path}.dds">
        <texture id="ui_decor_poster{some_texture_name}_page_1"               x="0"    y="0"    width="{w}"    height="{h}"/>
    </file>"""
            return tex_desc_template

        with open(wg_texture_descr_path + se + 'ui_rick_magazine.xml', 'w') as xml_desc2:
            xml_desc2.write('<w>')
            # xml_desc2.write('\n')

            dir_quer = 'SELECT path, name FROM TEXTURE_TABLE'


            for texture_name in sql.select_from(con=connec, direct_quer=dir_quer): 
                im = Image.open(f'{texture_name[0]}.dds')
                width, height = im.size
                if height == 2048:
                    xml_desc2.write(tex_desc_template_def(texture_name[0][-33:], texture_name[1][-9:], w=2048, h=2048))
                    xml_desc2.write('\n')
                else:
                    xml_desc2.write(tex_desc_template_def(texture_name[0][-33:], texture_name[1][-9:]))
                    xml_desc2.write('\n')
            xml_desc2.write('</w>')

        print('Описание постеров записано')       

    def create_description_xml(connec):
        'Описание текстур постеров для WG'

        sql = m_db.SqlTextureDB()
            
        with open(description_rus_path + se + 'poster_descrip.xml', 'w') as xml_desc:
            xml_desc.write('<?xml version="1.0" encoding="windows-1251"?>')
            xml_desc.write('\n\n')
            xml_desc.write('<string_table>\n')
            for texture_name in sql.select_from(con=connec, query_num=1):
                mag_id = texture_name[0][6:8]
                desc_name = m_pi.descrip_identif(mag_id)
                xml_desc.write(poster_item_descr(
                    num=texture_name[0][6:],
                    rarity_id=texture_name[0][9:10],
                    descript=desc_name[0],
                    poster_name=desc_name[1],
                    post_numb=texture_name[5]
                    )
                )
                xml_desc.write('\n')
            xml_desc.write('</string_table>')
        print('Описание текстур постеров записано')



    def way_writer(connec):
        '''Прописывает вручную пути текстур в файле меша
        Читай инструкцию внимательно!
        Требуется OGF tool:
        https://github.com/VaIeroK/OGF-tool/releases?ysclid=m8h7kmf2fx224135460'''
        
        def clip_copy_boart(copy_text):
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(copy_text)
            win32clipboard.CloseClipboard()

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
                    time.sleep(0.3)

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
    
    def textures_delete(tex_path):
        'Очистить все папки с текстурами'

        for file in os.listdir(tex_path):
            file_p = tex_path + os.sep + file
            if os.path.isdir(file_p):
                textures_delete(file_p)
            else:
                os.remove(file_p)
                # print(file_p)
        print('Текстуры удалены')

    def menu_func_new():
        while True:

            inp = inquirer.select(
                message="Меню:",
                choices=[
                    Choice(value=1, name='1. Пересоздать БД с текстурами'),
                    Choice(value=2, name='2. Переименовать текстуры постеров и внести в БД'),
                    Choice(value=3, name='3. SELECT * БД'),
                    Choice(value=4, name='4. Записать айтемы для постеров в "items_new_posters_pos.ltx"'),
                    Choice(value=5, name='5. Создать меши для текстур постеров'),
                    Choice(value=6, name='6. Записать содержимое журналов(лутбоксы)'),
                    Choice(value=6, name='7. Записать содержимое журналов и плакатов (бумага)'),
                    Choice(value=7, name='8. Записать описание для постеров'),
                    Choice(value=8, name='9. Записать описание текступ для Western Goods'),
                    Choice(value=10, name='10. Указать пути текстур в файле меша. Никакие программы кроме Cmd\PowerShell не должны быть включены! (требуется OGF tool)'),
                    Choice(value=11, name='11. Очистить все папки с текстурами'),
                    Choice(value=None, name='0. Выход')
                ],
                default=None
            ).execute()

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
                poster_texture_descr_wg(connec=connection)
                input()
            elif inp == 10:
                inp_4 = input('Вы закрыли все окна в windows? (д/н)\n')
                if inp_3 in ('д', 'y'):
                    way_writer(connec=connection)
                else:
                    print('Ничего')
                input()
            elif inp == 11:
                inp_3 = input('Данное действие очистит все патки с текстурами, продолжить? (д/н)\n')
                if inp_3 in ('д', 'y'):
                    textures_delete(path)
                else:
                    print('Ничего')
                input()
            elif inp == None:
                break
            # else:
            #     break
                    


    # def menu_func():
    #     while True:
    #         # print_slow('''
    #         print('''
    #         Меню:\n
    #         1. Пересоздать БД с текстурами
    #         2. Переименовать текстуры постеров и внести в БД
    #         3. SELECT * БД
    #         4. Записать айтемы для постеров в "items_new_posters_pos.ltx"
    #         5. Создать меши для текстур постеров
    #         6. Записать содержимое журналов(лутбоксы)
    #         7. Записать содержимое журналов и плакатов (бумага)
    #         8. Записать описание для постеров
    #         9. Записать описание текступ для Western Goods
    #         10. Указать пути текстур в файле меша. Никакие программы кроме Cmd\PowerShell не должны быть включены! (требуется OGF tool)
    #         11. Очистить все папки с текстурами
    #         0. Выход
    #         ''')
    #         try:
    #             inp = int(input('\nВвод: '))
    #         except:
    #             inp = 100
    #         sql_class = m_db.SqlTextureDB()

    #         if inp == 1:
    #             sql_class.create_tab(connection)
    #             input()
    #         elif inp == 2:
    #             sql_class.delete_from(connection)
    #             input()
    #             rename_files(texture_list)
    #             input()
    #             sql_class.insert_data(connection, texture_list)
    #             input()
    #         elif inp == 3:
    #             num = 0
    #             for i in sql_class.select_from(connection):
    #                 num += 1
    #                 print(f'{num}. {i}')
    #             input()
    #         elif inp == 4:
    #             create_poster_items(connec=connection)
    #             input()
    #         elif inp == 5:
    #             inp_2 = input('Данное действие перезапишет все меши, продолжить? (д/н)')
    #             if inp_2 in ('д', 'y'):
    #                 copy_poster_mesh(connec=connection, del_mesh=1)
    #             else:
    #                 print('Ничего')
    #             input()
    #         elif inp == 6:
    #             create_lootbox_content(connec=connection)
    #             input()
    #         elif inp == 7:
    #             create_items_parts_paper()
    #             input()
    #         elif inp == 8:
    #             create_description_xml(connec=connection)
    #             input()
    #         elif inp == 9:
    #             poster_texture_descr_wg(connec=connection)
    #             input()
    #         elif inp == 10:
    #             inp_4 = input('Вы закрыли все окна в windows? (д/н)\n')
    #             if inp_3 in ('д', 'y'):
    #                 way_writer(connec=connection)
    #             else:
    #                 print('Ничего')
    #             input()
    #         elif inp == 11:
    #             inp_3 = input('Данное действие очистит все патки с текстурами, продолжить? (д/н)\n')
    #             if inp_3 in ('д', 'y'):
    #                 textures_delete(path)
    #             else:
    #                 print('Ничего')
    #             input()
    #         elif inp == 0:
    #             break


    #         # elif inp == 25:
    #         #     num_3 = 0
    #         #     for i in sql_class.select_from(connection, query_num=1):
    #         #         num_3 += 1
    #         #         print(f'{num_3}. {i}')
    #         #     input()
            
            
    #         else:
    #             print('Ошибка, команда не найдена')
    #             input()
    
    # menu_func()

    menu_func_new()

if __name__ == '__main__':
        main()
    # try:
    # except Exception as err:
    #     print(err)

