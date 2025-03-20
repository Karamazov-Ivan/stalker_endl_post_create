def descrip_identif(magazine_id):
    if magazine_id == '03':
        descr = 'Японская манга. Выпуск #'
        mag_name = 'Постер из журнала "Японская манга"'
    elif magazine_id == '04':
        descr = 'Японсое аниме. Выпуск #'
        mag_name = 'Постер из журнала "Японсое аниме"'
    elif magazine_id == '05':
        descr = '"Maxim". Выпуск #'
        mag_name = 'Постер из журнала "Maxim"'
    elif magazine_id == '06':
        descr = '"FHM". Выпуск #'
        mag_name = 'Постер из журнала "FHM"'
    elif magazine_id == '07':
        descr = '"Grimm Fairy Tales". Выпуск #'
        mag_name = 'Постер из журнала "Grimm Fairy Tales"'
    elif magazine_id == '08':
        descr = '"Heavy Metal". Выпуск #'
        mag_name = 'Постер из журнала "Heavy Metal"'
    elif magazine_id == '09':
        descr = ':Журнал СССР "Крестьянка". Выпуск #'
        mag_name = 'Плакат СССР'
    elif magazine_id == '10':
        descr = 'Старый журнал (США). Выпуск #'
        mag_name = 'Постер из старого журнала США'
    elif magazine_id == '11':
        descr = '"Игромания". Выпуск #'
        mag_name = 'Постер из журнала "Игромания"'
    elif magazine_id == '12':
        descr = '"STALKER". Выпуск #'
        mag_name = 'Постер из журнала "STALKER"'
    elif magazine_id == '13':
        descr = 'Арт журнал. Выпуск #'
        mag_name = 'Постер из Арт журнала'
    elif magazine_id == '14':
        descr = 'Авто журнал СССР "За рулём". Выпуск #'
        mag_name = 'Плакат из журнала "За рулём"'
    elif magazine_id == '15':
        descr = 'Авто журнал Германия "Auto Bild". Выпуск #'
        mag_name = 'Постер из журнала "Auto Bild"'
    else:
        descr = 'некоторое описание'
        mag_name = 'некоторое название'
    
    return descr, mag_name

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