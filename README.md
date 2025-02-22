# RELIQUM

---

## ГЕЙМПЛЕЙНАЯ ЧАСТЬ

### ИГРОВОЙ ПРОЦЕСС:
Игроку-волшебнику необходимо избавить свой родной остров от вражеских захватчиков, для этого ему необходиомо уничтожить
17 врагов: 16 летучих глазов-приспешников и их предводителя могучего босса-бамбука. Чем быстрее игрок справится с этой
задачей, тем лучше, поэтому справа снизу ведётся подсчёт времени и количества уничтоженных врагов! Игрок имеет возможность
атаковать оружием: топор, копьё и использовать магию: огненный удар и лечение. Своё здоровье и энергию, а также выбранное оружие
можно увидеть внизу.
После убийства всех приспешников открывается доступ к двери, которая находится в самом верху игровой карты. Подойдя к ней можно войти в 
убежище босса и дать ему люлей! (или получить их). В конце игры вам любезно покажут за сколько вы справились с
поставленной задачей и сколько времени на это потратили. В случае поражения произойдет то же самое.
Топ 5 своих лучших забегов можно посмотреть в окне "Статистика" из главного меню.
В окне "Настройки", тоже в главно меню возможно изменить громкость музыки в меню и игре под свои нужды.

### УПРАВЛЕНИЕ:
Перемещение игрока производится на кнопки стрелочек: ← ↑ → ↓; Физический удар на Z, магический на X.
Смена оружия и магии происходит на кнопки Q и E соответственно. Кнопка ESC ставит игру на паузу, где будет отображено
написанное выше и позволяет выйти из неё в главное меню (без сохранения прогресса). На кнопку F4 можно изменить режим
экрана с полноэкранного на оконный и наоборот.

---

## ТЕХНИЧЕСКАЯ ЧАСТЬ

### СИСТЕМНЫЕ ТРЕБОВАНИЯ:
Около 500мб свободного места на диске.

### УСТАНОВКА:
Склонируйте репозиторий в желаемую папку с игрой и запустите файл Reliqum.exe (для ОС windows), либо main.py (для 
всевозможных ОС, но потребуется установка и настройка виратуального окружения).

### СТРУКТУРА ИГРЫ, НЕКОТОРЫЕ ОСОБЕННОСТИ:
Файлы, нужные для запуска игры лежат в папке Reliqum
Основными папками игры являются папки data, т.е. папка с данными (звуки, музыка, шрифты, уровни и т.п.) и source (
програмная часть игры, её логика, проще говоря, код). В папке data всё понятно из названий лежащих в ней файлов, а вот
про source стоит сказать несколько слов:

Окна игры по смыслу можно разделить на две части: **часть-меню** и **игровую**.
**menu** - папка с логикой игры со стороны меню, разделена на user_interface - код пользовательского интерфейса и 
menu_scripts - код непосредственно действий, происходящих в меню. main_stream.py - главный файл программы после main.py,
от которого исходит запуск меню и игры.
**helping_scripts** - некоторый код, являющийся вспомогательным, без возможности отнести его по тематике в какой-то
определенный подвид кода.
**game** - папка с логикой игры со стороны непосредственно игрового процесса. Разделена на user_interface - код пользовательского
интерфейса программы и game_scripts - код логики игры.

Подробное описание поведения игры можно получить из комментариев внутри кода. 

### ИСПОЛЬЗУЕМЫЕ ТЕХНОЛОГИИ:
ЯП python и его библиотеки: pygame, pygame_gui
---

**РАЗРАБОТЧИК ИГРЫ: SenioroPomidoro https://github.com/SenioroPomidoro**
