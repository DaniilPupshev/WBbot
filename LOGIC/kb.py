from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, WebAppInfo

from DATA_BASE import db
from LOGIC import config
from LOGIC.text import manual

db_process = db.options_db()

def create_set_shop_buttons(id_user):
    start_button = []

    tuple_name_shop = db_process.create_tuple_db_posizione(id_user, config.name_posizione[5])

    if tuple_name_shop[0] != None and len(tuple_name_shop) > 0:
        for i in tuple_name_shop[0].split('/')[:-1]:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_sh-{i}')])

    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_time_buttons(id_user):
    start_button = []

    type_user = db_process.get_type_user(id_user)

    id_admin = id_user

    check_admin = 0

    if type_user != 'owner':
        chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[17]))[0].split('/')
        use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
        id_use_shop = chek_shop.index(use_shop)

        tmp = db_process.create_tuple_db_posizione(id_user, config.name_posizione[16])[0].split('/')[id_use_shop]
        id_user = tmp

        check_admin = 1

    time_add = db_process.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')

    chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
    use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

    id_use_shop = chek_shop.index(use_shop)

    chek_name_company = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
    use_company = ''

    if check_admin == 1:
        use_company = list(db_process.create_tuple_db_posizione(id_admin, config.name_posizione[13]))[0]
    elif check_admin == 0:
        use_company = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]

    id_use_company = chek_name_company.index(use_company)

    tmp_time_add = time_add[id_use_shop].split('~')[id_use_company].split(';')

    if tmp_time_add[0] != None and len(tmp_time_add) > 0:
        for i in tmp_time_add:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dl_time-{i}')])

    if type_user == 'owner':
        start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])

    elif type_user == 'admin':
        start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_access_shop_buttons(id_user_admin):
    start_button = []

    if db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0] != None:
        tuple_name_shop_admin = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0].split('/')
        for i in tuple_name_shop_admin:
            if i != '':
                start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_sh_admin-{i}')])

    start_button.append([InlineKeyboardButton(text='Генератор QR-кодов', callback_data='gen_QR')])
    start_button.append([InlineKeyboardButton(text='Проверка позиций', callback_data='check_pozitione')])
    start_button.append([InlineKeyboardButton(text='Обновить магазины', callback_data='update_shop_admin')])
    start_button.append([InlineKeyboardButton(text='Выбор режима', callback_data='change_mode')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_access_shop_buttons_2(id_user_admin):
    start_button = []

    if db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0] != None:
        tuple_name_shop_admin = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0].split('/')
        for i in tuple_name_shop_admin:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_sh_admin-{i}')])

    start_button.append([InlineKeyboardButton(text='Генератор QR-кодов', callback_data='gen_QR')])
    start_button.append([InlineKeyboardButton(text='Проверка позиций', callback_data='check_pozitione')])
    start_button.append([InlineKeyboardButton(text='Выбор режима', callback_data='change_mode')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_access_company_buttons(id_user_admin):
    start_button = []

    admin_shop = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0].split('/')
    use_admin_shop = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[9])[0]

    id_use_shop = admin_shop.index(use_admin_shop)

    if db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[15])[0] != None:
        tuple_name_company_admin = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[15])[0].split('/')[id_use_shop].split(';')
        for i in tuple_name_company_admin:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_cp_admin-{i}')])

    start_button.append([InlineKeyboardButton(text='Обновить', callback_data='update_admin')])
    start_button.append([InlineKeyboardButton(text='Выбор режима', callback_data='change_mode')])
    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_access_company_buttons_2(id_user_admin):
    start_button = []

    admin_shop = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0].split('/')
    use_admin_shop = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[9])[0]

    id_use_shop = admin_shop.index(use_admin_shop)

    if db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[15])[0] != None:
        tuple_name_company_admin = db_process.create_tuple_db_posizione(id_user_admin, config.name_posizione[15])[0].split('/')[id_use_shop].split(';')
        for i in tuple_name_company_admin:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_cp_admin-{i}')])

    start_button.append([InlineKeyboardButton(text='Выбор режима', callback_data='change_mode')])
    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_company_buttons(id_user):
    start_button = []

    chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')[:-1]
    use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

    id_use_shop = chek_shop.index(use_shop)

    tuple_name_company = db_process.create_tuple_db_posizione(id_user, config.name_posizione[12])

    if tuple_name_company[0] != None and len(tuple_name_company) > 0:
        for i in tuple_name_company[0].split('/')[:-1][id_use_shop].split(';'):
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_cp-{i}')])

    start_button.append([InlineKeyboardButton(text='Изменить название', callback_data='change_name')])
    start_button.append([InlineKeyboardButton(text='Добавить админа', callback_data='add_admin')])
    start_button.append([InlineKeyboardButton(text='Удалить админа', callback_data='del_admin')])
    start_button.append([InlineKeyboardButton(text='Удалить магазин', callback_data='del_shop')])
    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_del_shop_buttons(id_user):
    start_button = []

    tuple_name_shop = db_process.create_tuple_db_posizione(id_user, config.name_posizione[5])

    if tuple_name_shop[0] != None and len(tuple_name_shop) > 0:
        for i in tuple_name_shop[0].split(';'):
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'del_sh-{i}')])

    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_admin_buttons(id_user):
    start_button = []

    admin_name = db_process.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')

    chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
    use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

    id_use_shop = chek_shop.index(use_shop)

    tmp_admin_name = admin_name[id_use_shop].split(';')

    if tmp_admin_name[0] != None and len(tmp_admin_name) > 0:
        for i in tmp_admin_name:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dl_admin-{i}')])

    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_in_company_buttons(id_user):
    start_button = []

    name_company = db_process.create_tuple_db_posizione(id_user, config.name_posizione[12])[0].split('/')

    chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
    use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

    id_use_shop = chek_shop.index(use_shop)

    chek_name_company = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
    use_company = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]

    id_use_company = chek_name_company.index(use_company)

    if ('Аукцион' not in name_company[id_use_shop].split(';')[id_use_company].split(' ')) or ('аукцион' not in name_company[id_use_shop].split(';')[id_use_company].split(' ')):
        start_button.append([InlineKeyboardButton(text='Отложенный запуск рекламы', callback_data='full_time')])
        start_button.append([InlineKeyboardButton(text='Зафиксировать ключевые запросы', callback_data='key_query')])
        start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
        start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
        return start_kb

    start_button.append([InlineKeyboardButton(text='Отложенный запуск рекламы', callback_data='full_time')])
    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

main_menu = [
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu'),
     ],
]

main_menu_admin = [
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin'),
     ],
]

stop = [
    [InlineKeyboardButton(text='Отмена', callback_data='cancellation'),
     ],
]

in_company = [
    [InlineKeyboardButton(text='Отложенный запуск рекламы', callback_data='full_time')
     ],
    [InlineKeyboardButton(text='Зафиксировать ключевые запросы', callback_data='key_query')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
     ],
]

in_company_admin = [
    [InlineKeyboardButton(text='Отложенный запуск рекламы', callback_data='full_time_admin')
     ],
    [InlineKeyboardButton(text='Зафиксировать ключевые запросы', callback_data='key_query_admin')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin')
     ],
]

time_button_admin = [
    [InlineKeyboardButton(text='Добавить запуск по времени', callback_data='time_start_add_admin')
     ],
    [InlineKeyboardButton(text='Удалить запуск по времени', callback_data='del_time_start_add_admin')
     ],
    [InlineKeyboardButton(text='Старт рекламы', callback_data='start_add')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin')
     ],
]

time_button_admin_2 = [
    [InlineKeyboardButton(text='Добавить запуск по времени', callback_data='time_start_add_admin')
     ],
    [InlineKeyboardButton(text='Удалить запуск по времени', callback_data='del_time_start_add_admin')
     ],
    [InlineKeyboardButton(text='Остановка рекламы', callback_data='stop_add')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_admin')
     ],
]

time_button = [
    [InlineKeyboardButton(text='Добавить запуск по времени', callback_data='time_start_add')
     ],
    [InlineKeyboardButton(text='Удалить запуск по времени', callback_data='del_time_start_add')
     ],
    [InlineKeyboardButton(text='Старт рекламы', callback_data='start_add')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
     ],
]

time_button_2 = [
    [InlineKeyboardButton(text='Добавить запуск по времени', callback_data='time_start_add')
     ],
    [InlineKeyboardButton(text='Удалить запуск по времени', callback_data='del_time_start_add')
     ],
    [InlineKeyboardButton(text='Остановка рекламы', callback_data='stop_add')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
     ],
]

start_button = [
    [InlineKeyboardButton(text='Добавить магазин', callback_data='add_shop')
     ],
    [InlineKeyboardButton(text='Список магазинов', callback_data='list_shop')
     ],
    [InlineKeyboardButton(text='Генератор QR-кодов', callback_data='gen_QR')
     ],
    [InlineKeyboardButton(text='Проверка позиций', callback_data='check_pozitione')
     ],
    [InlineKeyboardButton(text='Тарифы', callback_data='tariffs')
     ],
    [InlineKeyboardButton(text='Выбор режима', callback_data='change_mode')
     ],
]
tmp_manual = [
    [InlineKeyboardButton(text='Выбор режима', callback_data='change_mode')
     ],
]
start_button_2 = [
    [InlineKeyboardButton(text='Я менеджер', callback_data='reg_owner')
     ],
    [InlineKeyboardButton(text='Я администратор', callback_data='reg_admin')
     ],
    [InlineKeyboardButton(text='Инструкция', callback_data='manual')
     ],
]

in_company_kb = InlineKeyboardMarkup(inline_keyboard=in_company)
in_company_admin_kb = InlineKeyboardMarkup(inline_keyboard=in_company_admin)
menu = InlineKeyboardMarkup(inline_keyboard=main_menu)
menu_admin = InlineKeyboardMarkup(inline_keyboard=main_menu_admin)
start = InlineKeyboardMarkup(inline_keyboard=start_button)
start_2 = InlineKeyboardMarkup(inline_keyboard=start_button_2)
time = InlineKeyboardMarkup(inline_keyboard=time_button)
time_2 = InlineKeyboardMarkup(inline_keyboard=time_button_2)
time_admin = InlineKeyboardMarkup(inline_keyboard=time_button_admin)
time_admin_2 = InlineKeyboardMarkup(inline_keyboard=time_button_admin_2)
cancellation = InlineKeyboardMarkup(inline_keyboard=stop)
manual_kb = InlineKeyboardMarkup(inline_keyboard=tmp_manual)