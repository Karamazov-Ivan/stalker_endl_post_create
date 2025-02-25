import os
import time
import shutil
import win32clipboard
import sqlite3 as sl
import pyautogui as pau

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

    post_content_new_file = gamma_main_path + se + r'configs\items\settings\itms_manager_posters.ltx' # Содержимое журнала (лутбокс)

    post_parts_new_file = gamma_main_path + se + r'configs\items\settings\mod_parts_posters_3.ltx' # Части постеров и журналов для разборки (бумага)
    poster_mesh_path = gamma_main_path + se + r'meshes\dynamics\equipments\trade' # Меши журналов

    description_rus_path = gamma_main_path + se + r'configs\text\rus' # Описание айтемов, русский язык

    loot_quality_list = (
        'package_content',
        'package_content_uncommon',
        'package_content_rare',
        'package_content_epic',
        'package_content_legendary',
        'package_content_new_year',
        'package_content_spec'
        ) # Уровни редкости
    
    loot_quality_dict = {
        'package_content': 1,
        'package_content_uncommon': 2,
        'package_content_rare': 3,
        'package_content_epic': 4,
        'package_content_legendary': 5,
        'package_content_new_year': 6,
        'package_content_spec': 7
        } # Уровни редкости словарь

    class Sql_texture_db:

        def create_tab(self, con):
            with con:
                try:
                    con.execute('DROP TABLE TEXTURE_TABLE')
                except:
                    print('Таблица TEXTURE_TABLE не существует')
                con.execute("""
                    CREATE TABLE TEXTURE_TABLE (
                        name TEXT
                        ,TIMESTAMP_2 DEFAULT (datetime('now','localtime'))
                        ,path TEXT
                        --,magazine TEXT
                        --,rare TEXT
                        --,numb TEXT
                        --,TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            print('Таблица TEXTURE_TABLE создана')

        def insert_data(self, con, data):
            sql = 'INSERT INTO TEXTURE_TABLE (name, path) values(?, ?)'
            with con:
                con.executemany(sql, data)
            print('Данные текстур внесены в БД')

        def select_from(self, con, direct_quer=0, query_num=0):

            cursor = con.cursor()
            if query_num == 1:
                res = cursor.execute('''
                    SELECT *
                    FROM (
                        SELECT
                            name
                            ,SUBSTRING(name, 7, 2) AS mag
                            ,SUBSTRING(name, 10, 1) AS rare
                            ,SUBSTRING(name, 12, 4) AS numb
                        FROM TEXTURE_TABLE
                    ) AS result_t
                    --WHERE rare = '3'
                ''')
                return res.fetchall()
            
            elif query_num == 2:
                res = cursor.execute('''
                    SELECT name
                    FROM TEXTURE_TABLE
                ''')
                return res.fetchall()
            
            elif direct_quer:
                res = cursor.execute(direct_quer)
                return res.fetchall()
            
            else:
                res = cursor.execute('SELECT * FROM TEXTURE_TABLE')
                return res.fetchall()

            # if fetch:
            #     for row in res:
            #         print(row)

        def delete_from(self, con):
            with con:
                delete_table = 'TEXTURE_TABLE'
                con.execute(f'DELETE FROM {delete_table}')
            print(f'Таблица {delete_table} очищена')

    def rarity_identif(rarity_id):
        if rarity_id == '1':
            rar = r'%c[ui_gray_2]Обычный'
            cost = 20
        elif rarity_id == '2':
            rar = r'%c[0,0,128,0]Необычный'
            cost = 500
        elif rarity_id == '3':
            rar = r'%c[0,65,105,225]Редкий'
            cost = 3000
        elif rarity_id == '4':
            rar = r'%c[0,138,43,226]Эпический'
            cost = 10000
        elif rarity_id == '5':
            rar = r'%c[0,255,215,0]Легендарный'
            cost = 20000
        elif rarity_id == '6':
            rar = r'%c[0,178,34,34]Новогодний'
            cost = 23000
        elif rarity_id == '7':
            rar = r'%c[0,135,206,250]Специальный'
            cost = 23000
        else:
            rar = r'%c[d_red]Ошибочный'
            cost = 1

        return rar, cost

    def descrip_identif(magazine_id):
        print(type(magazine_id))
        if magazine_id == '03':
            descr = 'Японская манга. Выпуск #'
        elif magazine_id == '04':
            descr = 'Японсое аниме. Выпуск #'
        elif magazine_id == '05':
            descr = 'Журнал "Maxim". Выпуск #'
        elif magazine_id == '06':
            descr = 'Журнал "FHM". Выпуск #'
        elif magazine_id == '07':
            descr = 'Журнал комиксов "Grimm Fairy Tales". Выпуск #'
        elif magazine_id == '08':
            descr = 'Журнал "Heavy Metal". Выпуск #'
        elif magazine_id == '09':
            descr = 'Старый журнал (Азия). Выпуск #'
        elif magazine_id == '10':
            descr = 'Старый журнал (США). Выпуск #'
        elif magazine_id == '11':
            descr = 'Журнал "Игромания". Выпуск #'
        elif magazine_id == '12':
            descr = 'Журнал "STALKER". Выпуск #'
        else:
            descr = 'некоторое описание'
        
        return descr

    def print_slow(str_1):
        for letter in (str_1.split(' ')):
            stdout.write(letter + ' ')
            stdout.flush()
            time.sleep(0.01)

    def text_post(some_text, cost):
        total = rf""";=================POSTER_{some_text}
    [decor_poster{some_text}]:tch_junk
    class									= II_ATTCH
    kind								    = i_tool
    visual									= dynamics\efp_props\prop_poster_vertical_{some_text}.ogf

    description								= st_placeable_poster{some_text}_descr
    inv_name								= st_placeable_poster{some_text}
    inv_name_short							= st_placeable_poster{some_text}
    icons_texture							= ui\ui_maid_efp_props
    inv_grid_x								= 3
    inv_grid_y								= 5
    inv_grid_width							= 1
    inv_grid_height							= 2
    cost									= {cost}
    inv_weight								= 0.01
    use1_functor         				    = placeable_furniture.place_item
    use1_action_functor  					= placeable_furniture.func_place_item
    placeable_type                          = prop
    placeable_section                       = placeable_poster{some_text}

    snd_on_take								= paper
    repair_part_bonus	 	                = 0.02

    [placeable_poster{some_text}]:physic_object
    visual									= dynamics\efp_props\prop_poster_vertical_{some_text}.ogf
    placeable_type                          = prop
    base_rotation                           = 0
    script_binding                          = bind_hf_base.init
    item_section                            = decor_poster{some_text}
    ui_texture                              = ui_decor_poster{some_text}
    bounding_box_size                       = 0.570892, 0.747018, 0.017975
    bounding_box_origin                     = -0.02095, 0.012679, -0.005057"""

        return total

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
        sql = Sql_texture_db()
        with open(post_new_file, 'w') as f:
            for texture_name in sql.select_from(con=connec, query_num=2):
                tex_item_coun += 1
                rarity_id = texture_name[0][9:10]
                f.write(text_post(texture_name[0][6:], cost=rarity_identif(rarity_id)[1]))
                f.write('\n\n')
        print(f'Айтемы постеров созданы: {tex_item_coun} шт.')

    def copy_poster_mesh(connec, del_mesh=0):
        'Копирует меши и удаляет(опционально)'
        
        mes_coun = 0
        if del_mesh:
            for file in os.listdir(result_mes_path):
                os.remove(result_mes_path + se + file)

        sql = Sql_texture_db()            
        for texture_name in sql.select_from(con=connec, query_num=1):
            mes_coun += 1
            shutil.copy(mesh_ful_file_path, result_mes_path + os.sep + f'prop_poster_vertical_{texture_name[0][6:]}.ogf')
        print(f'Меши постеров созданы: {mes_coun}')

    def create_lootbox_content(connec):
        'Записывает содержимое (журналов)лутбоксов'

        sql = Sql_texture_db()

        with open(post_content_new_file, 'w') as pst_cont:

            for rare_name in loot_quality_list:
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
                        WHERE mag = '{mag_numb}' AND rare = '{loot_quality_dict[rare_name]}'
                    '''

                    sql_rar_mag_name = sql.select_from(con=connec, direct_quer=sql_rar_mag_code)
                    
                    pst_cont.write(f'new_mag_pos{mag_numb} = ' + ','.join([r[0] for r in sql_rar_mag_name]))
                    pst_cont.write('\n')
                pst_cont.write('\n')
        print('Содержимое журналов(лутбокс) записано')

    def create_items_parts_paper():
        'Дабавляет журналу/постеру часть Бумага 1шт. для разборки (Меши должны быть)'
        
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

    def poster_item_descr(num, rarity_id, descript):
        
        rar = rarity_identif(rarity_id)[0]
        poster_item_descr_text = rf'''
    <string id="st_placeable_poster{num}">
        <text>SOME_NAME</text>
    </string>
    <string id="st_placeable_poster{num}_descr">
        <text>%c[ui_gray_2]{descript}\n \n
        %c[0,255,255,255]РЕДКОСТЬ ВЫПУСКА: {rar}\n
        %c[ui_gray_2]ХАРАКТЕРИСТИКИ:\n
        %c[d_cyan] • %c[pda_white] Размещаемое\n
        </text>
    </string>'''
        return poster_item_descr_text

    def create_description_xml(connec):

        sql = Sql_texture_db()
            
        with open(description_rus_path + se + 'poster_descrip.xml', 'w') as xml_desc:
            xml_desc.write('<?xml version="1.0" encoding="windows-1251"?>')
            xml_desc.write('\n\n')
            xml_desc.write('<string_table>\n')
            for texture_name in sql.select_from(con=connec, query_num=2):
                mag_id = texture_name[0][6:8]
                xml_desc.write(poster_item_descr(num=texture_name[0][6:], rarity_id=texture_name[0][9:10], descript=descrip_identif(mag_id))) #, encoding='WINDOWS-1251', xml_declaration=True)
                xml_desc.write('\n')
            xml_desc.write('</string_table>')
        print('Описание постеров записано')

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

    def way_writer(connec):

        l_dir_work = os.listdir(result_mes_path)
        all_num = len(l_dir_work)
        cou = 1
        file_numb = 1
        sql = Sql_texture_db()
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

                    if cou:
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
            0. Выход
            ''')

            inp = int(input('\nВвод: '))
            sql_class = Sql_texture_db()

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
                copy_poster_mesh(connec=connection, del_mesh=1)
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
            elif inp == 0:
                break
            else:
                print('Ошибка, команда не найдена')
                input()
    
    menu_func()

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err)

