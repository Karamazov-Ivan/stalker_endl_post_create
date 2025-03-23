![изображение](https://github.com/user-attachments/assets/9fb205ee-c03b-42a9-be62-e1e061698613)## Описание
Это скрипт для добавления собственных постеров в мод для Stalker Anomaly [Endless posters Hideout Furniture](https://www.moddb.com/mods/stalker-anomaly/addons/endless-posters-hideout-furniture)

## Установка

Установите мод через МО2 [Endless posters Hideout Furniture](https://www.moddb.com/mods/stalker-anomaly/addons/endless-posters-hideout-furniture)

Установите Python, если у вас его нет [Инструкция с картинками (Пикабу)](https://pikabu.ru/story/zagruzka_i_ustanovka_python_10446605)

Тестировалось на версии 3.11

Скачайте файл [Stalker_endl_post_create](https://github.com/Karamazov-Ivan/stalker_endl_post_create/releases/tag/v1.0.9)

![изображение](https://github.com/user-attachments/assets/c0f7313d-ef53-4603-9703-167d4d72745a)

Распакуйте в любое место откройте файл config.ini

![изображение](https://github.com/user-attachments/assets/313bac7f-0b3c-4bd2-88c2-db9dc38375cd)

Укажите ваш путь в таком же формате к папке "gamedata" с модом сохраните и закройте

![изображение](https://github.com/user-attachments/assets/79edf750-ad96-40ef-a60e-80eebc7669e4)

Запустите файл "start_windows.bat"

![изображение](https://github.com/user-attachments/assets/be6cb2a4-41fb-44a7-a4e0-83fef7f0b852)

Появится меню (управление стрелками\цифрами):

![изображение](https://github.com/user-attachments/assets/5051fb26-a911-409d-8468-aa81112c3045)

Если вы дошли до этого момента и у вас не возникло ошибок, вы можете закрыть программу и приступить к подготовке изображений.


## Подготовка изображений

Теоретически у вас есть множество вариантов подготовить большое количество картинок. И вы можете придумать свой метод и поделиться им в комментариях. Я расскажу о своём способе.

Вам понадобится:

1. Photoshop

2. [NVIDIA Texture Tools Exporter](https://developer.nvidia.com/texture-tools-exporter) для работы с DDS

Соберите в одну папку картинки, которые хотите добавить. Обязательно сделайте резервную копию, так как они будёт перезаписаны! (Картинки в папке-источнике перезаписываются, их качество может измениться. Поэтому после обработки их надо удалить)

Затем разделите их на горизонтальные и вертикальные. (Воспользуйтесь файлом "image_sieve.py", который лежит в архиве, если хотите)

Включите Photoshop. В ранее распакованной папке найдите файл "add\Stalker_poster.atn" и кликните по нему 2 раза.

У вас появится такой "экшн"

![изображение](https://github.com/user-attachments/assets/5128eb57-3414-45a4-b40b-63db006023b1)

В папке "add" найдите архив "poster_templ.7z" и откройте один из файлов. Обычный для вертикальных картинок, "hor" - для горизонтальных.

Выберите этот слой (ЛКМ)

![изображение](https://github.com/user-attachments/assets/b30d1262-0468-4aa3-bc15-8691159be0ba)

Редактирование > Настройки цветов

Убрать галочки

![изображение](https://github.com/user-attachments/assets/84a29ac5-8b11-4cdb-83b4-242512e66d1a)

Файл > Автоматизация > Пакетная обработка

![изображение](https://github.com/user-attachments/assets/62e5d6b2-e53e-4c34-ae69-771e8393bf06)

Выберите "экшн", папку входа, выхода и прочие настройки

Запустите.

То же проделайте с изображениями другой ориентации при необходимости.

Итоговые картинки должны иметь формат .dds

## Интеграци изображений в мод

На этом примере покажу как добавить новые картинки в уже существующие журналы.

В папке "...\endless_posters_Hideout Furniture - Ivan\gamedata\textures\item\posters" выберите журнал, например 5-й.

Ниже расшифровка id каждой папки. "Специальный" подразумевался как широкоформатный, но сейчас вы можете использовать этот раздел как угодно, например для необычных и самых красивых изображений.

![изображение](https://github.com/user-attachments/assets/57e8495f-daa7-4bb2-8f8f-afae26b55676)

Распределите изображения по папкам по своему вкусу.

## Скрипт

Запустите файл "start_windows.bat"

![изображение](https://github.com/user-attachments/assets/be6cb2a4-41fb-44a7-a4e0-83fef7f0b852)

И запустите первые 2 пункта по очереди. Вы должны получить положительные сообщения.




