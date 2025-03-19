import uuid
from datetime import datetime, timedelta
import sqlite3
import time
import base64
import json

import asyncio
import aiosqlite
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from API_WB import api
from API_WB.api import set_negative_keywords_without_match
from LOGIC import config

wb_api = api.work_api()

scheduler = AsyncIOScheduler()

semaphore = asyncio.Semaphore(100)

class options_db():
    def __init__(self):
        self.name_db = 'database.db'

    def add_user(self, id_user, owner_nick, status_bot, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        if owner_nick == None:
            owner_nick = ''

        if self.check_user(id_user):
            return True, text_msg
        cur.execute(
            'REPLACE INTO Users (id_user, owner_nick, status_bot) VALUES (?, ?, ?)',
            (
                id_user,
                '@' + owner_nick,
                status_bot,
            )
        )
        con.commit()
        con.close()
        return False, text_msg

    def check_user(self, id_user):

        user_check = self.create_tuple_db_posizione(id_user, config.name_posizione[0])
        if (user_check != None) and (id_user in user_check):
            return True
        return False

    def create_list_column(self, type_column):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        cur.execute(f'SELECT {type_column} From Users')
        ret_l = cur.fetchall()
        return ret_l

    def reg_user(self, id_user, type_user, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        cur.execute('UPDATE Users SET type_user = ? WHERE id_user = ?', (type_user, id_user))
        con.commit()
        return text_msg[0]

    def get_id_shop_company(self, id_user):
        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        id_use_company = None

        if list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0] != None:

            chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
            use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]

            id_use_company = chek_name_company.index(use_company)

        return id_use_shop, id_use_company


    def reg_admin(self, id_user_admin, type_user, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        owner_admin = self.create_tuple_db_posizione(id_user_admin, config.name_posizione[16])[0]

        if owner_admin != None:
            cur.execute('UPDATE Users SET admin_company = ? WHERE id_user = ?', (None, id_user_admin))
            cur.execute('UPDATE Users SET owner_admin = ? WHERE id_user = ?', (None, id_user_admin))

        cur.execute(f'SELECT id_admin From Users')

        column_id_admin = cur.fetchall()

        all_column_id_admin = []

        for i in range(len(column_id_admin)):
            if column_id_admin[i][0] != None:
                for j in range(len(column_id_admin[i][0].split('/'))):
                    if column_id_admin[i][0].split('/')[j] != '':
                        for k in range(len(column_id_admin[i][0].split('/')[j].split('~'))):
                            if column_id_admin[i][0].split('/')[j].split('~')[k] != '':
                                for m in range(len(column_id_admin[i][0].split('/')[j].split('~')[k].split(';'))):
                                    if column_id_admin[i][0].split('/')[j].split('~')[k].split(';')[m] != '':
                                        all_column_id_admin.append(column_id_admin[i][0].split('/')[j].split('~')[k].split(';')[m])

        if str(id_user_admin) in all_column_id_admin:
            cur.execute('UPDATE Users SET type_user = ? WHERE id_user = ?', (type_user, id_user_admin))

            column_id_user = self.create_list_column('id_user')
            tmp_column_id_admin = self.create_list_column('id_admin')

            column_id_admin_2 = []

            for i in range(len(tmp_column_id_admin)):
                if tmp_column_id_admin[i][0] != None:
                    column_id_admin_2.append([tmp_column_id_admin[i][0].split('/')[j].split('~') for j in range(len(tmp_column_id_admin[i][0].split('/'))) if tmp_column_id_admin[i][0].split('/')[j] != ''])

            ids = []
            ids_id_user = []

            for i in range(len(column_id_admin_2)):
                for j in range(len(column_id_admin_2[i])):
                    for k in range(len(column_id_admin_2[i][j])):
                        tmp = ''.join(column_id_admin_2[i][j][k]).split(';')[1:]
                        if str(id_user_admin) in tmp:
                            ids.append([j, k])
                            ids_id_user.append([j, k])
                        else:
                            ids.append([''])

            l_id_user = []
            tmp_l_name_company_admin = []
            ret_l_name_company_admin = []
            tmp_l_name_shop = []

            for i in range(len(ids_id_user)):
                id_user = str(column_id_user[0][0])
                l_id_user.append(id_user)

            for i in range(len(ids)):
                if ids[i][0] != '':

                    id_use_shop = ids[i][0]

                    for j in range(len(l_id_user)):
                        if self.create_tuple_db_posizione(l_id_user[j], config.name_posizione[12])[0] != None:
                            name_company = self.create_tuple_db_posizione(l_id_user[j], config.name_posizione[12])[0].split('/')[:-1][id_use_shop].split(';')
                            name_shop = self.create_tuple_db_posizione(l_id_user[j], config.name_posizione[5])[0].split('/')[id_use_shop]
                            tmp_l_name_shop.append(name_shop)
                            for name in name_company:
                                tmp_l_name_company_admin.append(name)

            l_name_company_admin = list(set(tmp_l_name_company_admin))
            l_name_shop = list(set(tmp_l_name_shop))

            ret_l_name_company_admin.append(';'.join(l_name_company_admin))

            cur.execute('UPDATE Users SET admin_company = ? WHERE id_user = ?', ('/'.join(ret_l_name_company_admin) + '/', id_user_admin))
            cur.execute('UPDATE Users SET owner_admin = ? WHERE id_user = ?', ('/'.join(l_id_user) + '/', id_user_admin))
            cur.execute('UPDATE Users SET admin_shop = ? WHERE id_user = ?', ('/'.join(l_name_shop) + '/', id_user_admin))

            con.commit()
            return text_msg[0]
        return text_msg[1]

    def check_status(self, id_user, checked_status):

        db_status = self.create_tuple_db_posizione(id_user, config.name_posizione[2])
        if (db_status != None) and (db_status[0] == checked_status):
            return True
        return False

    def check_text(self, checked_text):
        tmp = checked_text
        if ';' in tmp:
            tmp = checked_text.replace(';', '')
        return ''.join(tmp)

    import time
    def check_time_format(self, checked_time):
        try:
            time.strptime(checked_time, '%H:%M')
            return True
        except ValueError:
            return False

    def get_type_user(self, id_user):
        type_user = self.create_tuple_db_posizione(id_user, config.name_posizione[14])[0]
        return type_user

    def cancellation_token(self, id_user, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', (config.statuses[0], id_user))

        chek_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[5])

        count_shop = (list(chek_shop)[0]).split('/')
        del count_shop[-2]

        if len(count_shop) > 1:
            cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(count_shop) + '/', id_user))
            con.commit()

        else:
            cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (None, id_user))
            con.commit()
        return text_msg[0]

    def create_tuple_db_posizione(self, id_user, name_posizione):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        db_posizione = cur.execute(f'SELECT {name_posizione} FROM Users WHERE id_user = {id_user}').fetchone()
        con.commit()
        return db_posizione

    def change_status(self, id_user, new_status, text_msg, check):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        if check == 'st_b':
            if self.check_user(id_user):
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', (new_status, id_user))
                con.commit()
                return text_msg[0]

        elif check == 'st_sh':
            if self.check_user(id_user):
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', (config.statuses[3], id_user))
                cur.execute('UPDATE Users SET use_shop = ? WHERE id_user = ?', (new_status, id_user))
                con.commit()
                return text_msg[0]

        elif check == 'st_cp':
            if self.check_user(id_user):
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', (config.statuses[12], id_user))
                cur.execute('UPDATE Users SET use_company = ? WHERE id_user = ?', (new_status, id_user))
                con.commit()
                return text_msg[0]

        return text_msg[1]

    def key_query(self, id_user, text_phrases, text_msg):

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]

        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        my_phrases = text_phrases.split('\n')

        res = set_negative_keywords_without_match(use_token, my_phrases, id_use_company_id)
        if res == 200:
            return text_msg[0]
        return text_msg[1]


    def add_shop(self, id_user, name_shop, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        shop = self.check_text(name_shop)
        chek_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[5])

        if len(name_shop) > 0:
            if chek_shop[0] != None:
                count_shop = (list(chek_shop)[0]).split('/')
                count_shop[-1] = shop

                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(count_shop) + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('add_token', id_user))

            elif chek_shop[0] == None:
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (shop + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('add_token', id_user))

            con.commit()
            return text_msg[0]
        return text_msg[1]

    def change_name_shop(self, id_user, new_name):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        name = self.check_text(new_name)

        id_use_shop = self.get_id_shop_company(id_user)[0]

        tmp = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        tmp[id_use_shop] = name

        cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(tmp), id_user))
        cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
        con.commit()

        return 'Название магазина изменено'

    async def ret_pozitione(self, tmp_text, id_user):
        async with aiosqlite.connect(self.name_db) as con:
            cur = await con.cursor()

            text = tmp_text.split(' ', maxsplit=1)

            n = set(range(10))
            count = sum(1 for char in text[0] if char.isdigit())

            if len(text) < 2 or count != len(text[0]):
                text_msg = 'Неверный формат команды.\nПример: 12345678 перчатки мужские'
                return text_msg

            target_artikul = text[0]
            key_word = text[1]

            position = await api.start(target_artikul, key_word)

            if position is not None:
                text_msg = f"Артикул {target_artikul} найден на позиции {position + 1} по запросу '{key_word}'."
            else:
                text_msg = f"Артикул {target_artikul} не найден по запросу '{key_word}'."

            await cur.execute(
                'UPDATE Users SET status_bot = ? WHERE id_user = ?',
                ('waiting', id_user)
            )
            await con.commit()

            return text_msg

    def decode_base64url(self, data):
        padded = data + '=' * (4 - len(data) % 4)
        return base64.urlsafe_b64decode(padded).decode('utf-8')

    def add_token(self, id_user, text_token, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        token = self.check_text(text_token)
        check_token = self.create_tuple_db_posizione(id_user, config.name_posizione[6])
        check_id_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[3])
        check_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])
        check_admin_name = self.create_tuple_db_posizione(id_user, config.name_posizione[7])
        check_id_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[4])
        check_id_token = self.create_tuple_db_posizione(id_user, config.name_posizione[10])
        check_name_company = self.create_tuple_db_posizione(id_user, config.name_posizione[12])
        check_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])
        check_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])

        if wb_api.check_token(text_token):
            header_b64, payload_b64, signature_b64 = token.split('.')
            payload = json.loads(self.decode_base64url(payload_b64))
            sid = payload['sid']
            tmp_set_company = wb_api.get_full_list_campaign(token)

            set_name_company = []
            set_id_company = []

            for num_company in range(len(tmp_set_company)):
                set_name_company.append(str(tmp_set_company[num_company][0]))
                set_id_company.append(str(tmp_set_company[num_company][1]))

            if check_name_company[0] != None:
                count_token = list(check_token)[0].split('/')
                count_id_shop = list(check_id_shop)[0].split('/')
                count_time_add = list(check_time_add)[0].split('/')
                count_pull_add = list(check_pull_add)[0].split('/')
                count_admin_name = list(check_admin_name)[0].split('/')
                count_id_admin = list(check_id_admin)[0].split('/')
                count_id_token = list(check_id_token)[0].split('/')
                count_name_company = list(check_name_company)[0].split('/')
                count_task_id = list(check_task_id)[0].split('/')

                add_s = len(tmp_set_company) * '~'

                count_time_add.append(add_s)
                count_pull_add.append(add_s)
                count_admin_name.append(add_s)
                count_id_admin.append(add_s)
                count_task_id.append(add_s)

                if str(sid) in count_id_token:
                    chek_name_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))
                    tmp_check_name_shop = (list(chek_name_shop)[0]).split('/')
                    del tmp_check_name_shop[-2]
                    cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(tmp_check_name_shop) + '/', id_user))
                    cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                    con.commit()
                    return text_msg[1]

                count_token[-1] = token
                count_id_token[-1] = str(sid)

                for name_company in set_name_company:
                    count_name_company[-1] += name_company

                for id_company in set_id_company:
                    count_id_shop[-1] += id_company

                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', ('/'.join(count_token) + '/', id_user))
                cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', ('/'.join(count_time_add) + '/', id_user))
                cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ('/'.join(count_pull_add) + '/', id_user))
                cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ('/'.join(count_task_id) + '/', id_user))
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?',('/', id_user))
                cur.execute('UPDATE Users SET id_admin = ? WHERE id_user = ?',('/', id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', ('/'.join(count_name_company) + '/', id_user))
                cur.execute('UPDATE Users SET id_token = ? WHERE id_user = ?', ('/'.join(count_id_token) + '/', id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', ('/'.join(count_id_shop) + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))

            elif check_name_company[0] == None:
                tmp_set_company = wb_api.get_full_list_campaign(token)

                set_name_company = []
                set_id_company = []

                for num_company in range(len(tmp_set_company)):
                    set_name_company.append(str(tmp_set_company[num_company][0]))
                    set_id_company.append(str(tmp_set_company[num_company][1]))

                cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', ((len(tmp_set_company) * '~') + '/', id_user))
                cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ((len(tmp_set_company) * '~') + '/', id_user))
                cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ((len(tmp_set_company) * '~') + '/', id_user))
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?',('/', id_user))
                cur.execute('UPDATE Users SET id_admin = ? WHERE id_user = ?',('/', id_user))
                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', (token + '/', id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', (';'.join(set_name_company) + '/', id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', (';'.join(set_id_company) + '/', id_user))
                cur.execute('UPDATE Users SET id_token = ? WHERE id_user = ?', (str(sid) + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))

            con.commit()
            return text_msg[0]
        return text_msg[1]

    def replace_id(self, id_user):
        type_user = self.get_type_user(id_user)

        if type_user != 'owner':
            chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[17]))[0].split('/')
            use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
            id_use_shop = chek_shop.index(use_shop)

            tmp = self.create_tuple_db_posizione(id_user, config.name_posizione[16])[0].split('/')[id_use_shop]
            id_user = tmp

        return id_user

    def get_budget_campaign(self, id_user, use_company):
        id_user = self.replace_id(id_user)

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
        id_use_shop = chek_shop.index(use_shop)

        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        budget_campaign = wb_api.budget_campaign(use_token, int(id_use_company_id))

        return budget_campaign

    def ret_use_company(self, id_user):
        id_user = self.replace_id(id_user)

        use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]
        return use_company

    def get_all_info_company(self, id_user, use_company):
        id_user = self.replace_id(id_user)

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
        id_use_shop = chek_shop.index(use_shop)

        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        info_campaign = wb_api.get_info_campaign(use_token, int(id_use_company_id))

        return info_campaign

    def start_add(self, id_user):
        id_user = self.replace_id(id_user)

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
        id_use_shop = chek_shop.index(use_shop)

        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]
        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        info_campaign = self.get_all_info_company(id_user, use_company)
        name = info_campaign['name']

        text_msg = f'Компания {name} запущена'

        response = wb_api.start_campaign(use_token, int(id_use_company_id))

        if response.status_code == 200:
            text_msg = f'Компания {name} запущена'
        else:
            text_msg = 'Ошибка'

        return text_msg

    def stop_add(self, id_user):
        id_user = self.replace_id(id_user)

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
        id_use_shop = chek_shop.index(use_shop)

        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]
        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        info_campaign = wb_api.get_info_campaign(use_token, int(id_use_company_id))
        name = info_campaign['name']

        text_msg = f'Компания {name} остановлена'
        response = wb_api.pause_campaign(use_token, int(id_use_company_id))

        if response.status_code == 200:
            text_msg = f'Компания {name} остановлена'
        else:
            text_msg = 'Ошибка'

        return text_msg

    def add_admin(self, id_user, id_ad, text_msg, nick_user):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        nick = self.check_text(nick_user)

        all_colum_id_user = self.create_list_column('id_user')

        admin_name = self.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')
        id_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[4])[0].split('/')

        id_user_db = self.create_tuple_db_posizione(id_user, config.name_posizione[0])[0]

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        check = 0

        for i in range(len(all_colum_id_user)):
            if str(all_colum_id_user[i][0]) == str(id_ad):
                check = 1

        if (len(id_admin) > 0) and (str(id_ad) != id_user_db) and (check == 1):
            if (admin_name[0] != None) and (f'@{nick}' not in (list(admin_name)[0]).split('/')[id_use_shop].split(';')):
                tmp_admin_name = admin_name[id_use_shop].split(';')
                tmp_id_admin = id_admin[id_use_shop].split(';')

                tmp_admin_name.append(f'@{nick}')
                tmp_id_admin.append(id_ad)

                check_admin_name = self.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')
                check_id_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[4])[0].split('/')

                check_admin_name[id_use_shop] = ';'.join(tmp_admin_name)
                check_id_admin[id_use_shop] = ';'.join(tmp_id_admin)

                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', ('/'.join(check_admin_name), id_user))
                cur.execute('UPDATE Users SET id_admin = ? WHERE id_user = ?', ('/'.join(check_id_admin), id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                con.commit()
                return text_msg[0]
        con.commit()
        return text_msg[1]

    def del_admin(self, id_user, text_msg, nick_user):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        nick = self.check_text(nick_user)

        admin_name = self.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')
        id_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[4])[0].split('/')

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        tmp_admin_name = admin_name[id_use_shop].split(';')
        tmp_id_admin = id_admin[id_use_shop].split(';')

        id_del = tmp_admin_name.index(nick)

        id_del_admin = tmp_id_admin[id_del]

        del tmp_admin_name[id_del]
        del tmp_id_admin[id_del]

        if self.create_tuple_db_posizione(id_del_admin, config.name_posizione[16])[0] != None:

            tmp_owner_admin = self.create_tuple_db_posizione(id_del_admin, config.name_posizione[16])[0].split('/')
            tmp_admin_company = self.create_tuple_db_posizione(id_del_admin, config.name_posizione[15])[0].split('/')

            del tmp_admin_company[tmp_owner_admin.index(str(id_user))]
            del tmp_owner_admin[tmp_owner_admin.index(str(id_user))]

            if tmp_owner_admin == [] or tmp_owner_admin[0] == '':
                cur.execute('UPDATE Users SET owner_admin = ? WHERE id_user = ?', (None, id_del_admin))
                cur.execute('UPDATE Users SET admin_company = ? WHERE id_user = ?', (None, id_del_admin))
            else:
                cur.execute('UPDATE Users SET owner_admin = ? WHERE id_user = ?', ('/'.join(tmp_owner_admin), id_del_admin))
                cur.execute('UPDATE Users SET admin_company = ? WHERE id_user = ?', ('/'.join(tmp_admin_company), id_del_admin))

        check_admin_name = self.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')
        check_id_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[4])[0].split('/')
        check_admin_name[id_use_shop] = ';'.join(tmp_admin_name)
        check_id_admin[id_use_shop] = ';'.join(tmp_id_admin)

        cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', ('/'.join(check_admin_name), id_user))
        cur.execute('UPDATE Users SET id_admin = ? WHERE id_user = ?', ('/'.join(check_id_admin), id_user))
        cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
        con.commit()
        return text_msg[0]

    def parse_time(self, time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def chek_interval(self, id_user, new_interval, id_use_shop, id_use_company):
        intervals = list(self.create_tuple_db_posizione(id_user, config.name_posizione[8]))[0].split('/')[id_use_shop].split('~')[id_use_company].split(';')[1:]

        start_str, end_str = new_interval.split('-')
        start_new = self.parse_time(start_str)
        end_new = self.parse_time(end_str)

        if end_new < start_new:
            first_part = (start_new, 24 * 60)
            second_part = (0, end_new)
        else:
            first_part = (start_new, end_new)
            second_part = None

        for interval in intervals:
            start_str, end_str = interval.split('-')
            start_existing = self.parse_time(start_str)
            end_existing = self.parse_time(end_str)

            if end_existing < start_existing:
                existing_first_part = (start_existing, 24 * 60)
                existing_second_part = (0, end_existing)
            else:
                existing_first_part = (start_existing, end_existing)
                existing_second_part = None

            if (first_part[0] < existing_first_part[1] and existing_first_part[0] < first_part[1]):
                return True

            if second_part and existing_second_part:
                if (second_part[0] < existing_second_part[1] and existing_second_part[0] < second_part[1]):
                    return True
        return False

    async def execute_task(self, id_user, start_time, end_time):
        id_user = self.replace_id(id_user)

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
        id_use_shop = chek_shop.index(use_shop)

        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]
        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        await wb_api.start_campaign1(use_token, id_use_company_id, id_user)

        while True:
            current_time = datetime.now().strftime('%H:%M')
            if current_time >= end_time:
                break
            time.sleep(1)

        await wb_api.pause_campaign1(use_token, id_use_company_id, id_user)

    def schedule_task(self, id_user, start_time, end_time, task_id):
        now = datetime.now()
        task_start_time = datetime.strptime(f"{now.date()} {start_time}", '%Y-%m-%d %H:%M')
        if task_start_time < now:
            task_start_time += timedelta(days=1)

        scheduler.add_job(
            self.execute_task,
            'date',
            run_date=task_start_time,
            args=(id_user, task_id, end_time),
            id=f"task_{task_id}"
        )

    def remove_task(self, id_user, use_token, id_use_company_id, task_id):
        if scheduler.get_job(f"task_{task_id}"):
            # wb_api.pause_campaign1(use_token, id_use_company_id, id_user)
            scheduler.remove_job(f"task_{task_id}")

    def start_scheduler(self):
        scheduler.start()

    def add_time(self, id_user, checked_text, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        type_user = self.get_type_user(id_user)

        id_admin = id_user

        flag = 0

        check_admin = 0

        if type_user != 'owner':
            chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[17]))[0].split('/')
            use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
            id_use_shop = chek_shop.index(use_shop)

            tmp = self.create_tuple_db_posizione(id_user, config.name_posizione[16])[0].split('/')[id_use_shop]
            id_user = tmp

            check_admin = 1

            flag = 1

        time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
        pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')
        l_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        use_company = ''

        if check_admin == 1:
            use_company = list(self.create_tuple_db_posizione(id_admin, config.name_posizione[13]))[0]
        elif check_admin == 0:
            use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]

        id_use_company = chek_name_company.index(use_company)

        text_time = self.check_text(checked_text)

        count = 0

        for i in range(len(time_add[0].split('~'))):
            if time_add[0].split('~')[i] == '':
                count += 1

        if self.check_time_format(text_time[:5]) and self.check_time_format(text_time[-5:]) and len(text_time) == 11 and len(text_time.split('-')) == 2:
            task_id = uuid.uuid4().hex
            if len(time_add[0].split('~')) != count:
                if not self.chek_interval(id_user, text_time, id_use_shop, id_use_company):
                    tmp_time_add = time_add[id_use_shop].split('~')[id_use_company].split(';')
                    tmp_pull_add = pull_add[id_use_shop].split('~')[id_use_company].split(';')
                    tmp_task_id = l_task_id[id_use_shop].split('~')[id_use_company].split(';')

                    tmp_time_add.append(text_time)
                    tmp_pull_add.append('stop')
                    tmp_task_id.append(task_id)

                    check_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')[id_use_shop].split('~')
                    check_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')[id_use_shop].split('~')
                    check_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')[id_use_shop].split('~')

                    check_time_add[id_use_company] = ';'.join(tmp_time_add)
                    check_pull_add[id_use_company] = ';'.join(tmp_pull_add)
                    check_task_id[id_use_company] = ';'.join(tmp_task_id)

                    check2_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
                    check2_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')
                    check2_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')

                    check2_time_add[id_use_shop] = '~'.join(check_time_add)
                    check2_pull_add[id_use_shop] = '~'.join(check_pull_add)
                    check2_task_id[id_use_shop] = '~'.join(check_task_id)

                    self.schedule_task(id_user, text_time[:5], text_time[-5:], task_id)

                    cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', ('/'.join(check2_time_add), id_user))
                    cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ('/'.join(check2_pull_add), id_user))
                    cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ('/'.join(check2_task_id), id_user))
                    cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                    con.commit()
                    return text_msg[0], flag
                con.commit()
                return text_msg[1], flag

            elif len(time_add[0].split('~')) == count:
                tmp_time_add = time_add[id_use_shop].split('~')[id_use_company].split(';')
                tmp_pull_add = pull_add[id_use_shop].split('~')[id_use_company].split(';')
                tmp_task_id = l_task_id[id_use_shop].split('~')[id_use_company].split(';')

                tmp_time_add.append(text_time)
                tmp_pull_add.append('stop')
                tmp_task_id.append(task_id)

                check_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')[id_use_shop].split('~')
                check_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')[id_use_shop].split('~')
                check_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')[id_use_shop].split('~')

                check_time_add[id_use_company] = ';'.join(tmp_time_add)
                check_pull_add[id_use_company] = ';'.join(tmp_pull_add)
                check_task_id[id_use_company] = ';'.join(tmp_task_id)

                check2_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
                check2_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')
                check2_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')

                check2_time_add[id_use_shop] = '~'.join(check_time_add)
                check2_pull_add[id_use_shop] = '~'.join(check_pull_add)
                check2_task_id[id_use_shop] = '~'.join(check_task_id)

                self.schedule_task(id_user, text_time[:5], text_time[-5:], task_id)

                cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', ('/'.join(check2_time_add), id_user))
                cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ('/'.join(check2_pull_add), id_user))
                cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ('/'.join(check2_task_id), id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                con.commit()
                return text_msg[0], flag
        con.commit()
        return text_msg[1], flag

    def del_time(self, id_user, text_time, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        type_user = self.get_type_user(id_user)

        id_admin = id_user

        check_admin = 0

        if type_user != 'owner':
            chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[17]))[0].split('/')
            use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]
            id_use_shop = chek_shop.index(use_shop)

            tmp = self.create_tuple_db_posizione(id_user, config.name_posizione[16])[0].split('/')[id_use_shop]
            id_user = tmp

            check_admin = 1

        time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
        pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')
        l_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')

        id_use_shop = self.get_id_shop_company(id_user)[0]
        use_token = list(self.create_tuple_db_posizione(id_user, config.name_posizione[6]))[0].split('/')[id_use_shop]

        chek_name_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[12]))[0].split('/')[:-1][id_use_shop].split(';')
        use_company = ''

        if check_admin == 1:
            use_company = list(self.create_tuple_db_posizione(id_admin, config.name_posizione[13]))[0]
        elif check_admin == 0:
            use_company = list(self.create_tuple_db_posizione(id_user, config.name_posizione[13]))[0]
        id_use_company = chek_name_company.index(use_company)

        id_use_company_id = list(self.create_tuple_db_posizione(id_user, config.name_posizione[3]))[0].split('/')[:-1][id_use_shop].split(';')[id_use_company]

        tmp_time_add = time_add[id_use_shop].split('~')[id_use_company].split(';')
        tmp_pull_add = pull_add[id_use_shop].split('~')[id_use_company].split(';')
        tmp_task_id = l_task_id[id_use_shop].split('~')[id_use_company].split(';')

        id_time = tmp_time_add.index(text_time)

        unic_task_id = tmp_task_id[id_time]

        del tmp_time_add[id_time]
        del tmp_pull_add[id_time]
        del tmp_task_id[id_time]

        check_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')[id_use_shop].split('~')
        check_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')[id_use_shop].split('~')
        check_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')[id_use_shop].split('~')

        check_time_add[id_use_company] = ';'.join(tmp_time_add)
        check_pull_add[id_use_company] = ';'.join(tmp_pull_add)
        check_task_id[id_use_company] = ';'.join(tmp_task_id)

        check2_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
        check2_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])[0].split('/')
        check2_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')

        check2_time_add[id_use_shop] = '~'.join(check_time_add)
        check2_pull_add[id_use_shop] = '~'.join(check_pull_add)
        check2_task_id[id_use_shop] = '~'.join(check_task_id)

        self.remove_task(id_user, use_token, id_use_company_id, unic_task_id)

        cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', ('/'.join(check2_time_add), id_user))
        cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ('/'.join(check2_pull_add), id_user))
        cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ('/'.join(check2_task_id), id_user))
        cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
        con.commit()
        return text_msg[0]

    def del_shop(self, id_user, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        all_colum_id_user = self.create_list_column('id_user')

        chek_name_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))
        check_id_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[3])
        check_token = self.create_tuple_db_posizione(id_user, config.name_posizione[6])
        check_id_token = self.create_tuple_db_posizione(id_user, config.name_posizione[10])
        check_name_company = self.create_tuple_db_posizione(id_user, config.name_posizione[12])
        check_permission_user = self.create_tuple_db_posizione(id_user, config.name_posizione[7])
        check_id_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[4])
        check_time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])
        check_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])
        check_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])

        if chek_name_shop != None:
            tmp_check_name_shop = (list(chek_name_shop)[0]).split('/')
            tmp_check_id_shop = (list(check_id_shop)[0]).split('/')
            tmp_check_token = (list(check_token)[0]).split('/')
            tmp_id_token = (list(check_id_token)[0]).split('/')
            tmp_name_company = (list(check_name_company)[0]).split('/')
            tmp_permission_user = (list(check_permission_user)[0]).split('/')
            tmp_id_admin = (list(check_id_admin)[0]).split('/')
            tmp_time_add = (list(check_time_add)[0]).split('/')
            tmp_pull_add = (list(check_pull_add)[0]).split('/')
            tmp_task_id = (list(check_pull_add)[0]).split('/')

            id_use_shop = self.get_id_shop_company(id_user)[0]

            all_use_id_admin = tmp_id_admin[id_use_shop].split('~')

            del tmp_check_name_shop[id_use_shop]
            del tmp_check_id_shop[id_use_shop]
            del tmp_check_id_shop[id_use_shop]
            del tmp_id_token[id_use_shop]
            del tmp_name_company[id_use_shop]
            del tmp_permission_user[id_use_shop]
            del tmp_id_admin[id_use_shop]
            del tmp_time_add[id_use_shop]
            del tmp_pull_add[id_use_shop]
            del tmp_task_id[id_use_shop]

            all_ind_del_admin = []
            id_user_admin = ''

            for i in range(len(all_colum_id_user)):
                for j in range(len(all_use_id_admin)):
                    if ';' + str(all_colum_id_user[i][0]) == all_use_id_admin[j]:
                        id_user_admin = str(all_colum_id_user[i][0])
                        all_ind_del_admin.append(j)

            if (id_user_admin != '') and (self.create_tuple_db_posizione(id_user_admin, config.name_posizione[16]) != None):

                tmp_owner_admin = self.create_tuple_db_posizione(id_user_admin, config.name_posizione[16])[0].split('/')
                tmp_admin_company = self.create_tuple_db_posizione(id_user_admin, config.name_posizione[15])[0].split('/')
                tmp_admin_shop = self.create_tuple_db_posizione(id_user_admin, config.name_posizione[17])[0].split('/')
                tmp_task_id = self.create_tuple_db_posizione(id_user, config.name_posizione[18])[0].split('/')

                for ind in all_ind_del_admin:
                    tmp_owner_admin[ind] = ''
                    tmp_admin_company[ind] = ''
                    tmp_admin_shop[ind] = ''
                    tmp_task_id[ind] = ''

                owner_admin = [i for i in tmp_owner_admin if i != '']
                admin_company = [i for i in tmp_admin_company if i != '']
                admin_shop = [i for i in tmp_admin_shop if i != '']
                task_id = [i for i in tmp_task_id if i != '']

                if owner_admin == []:
                    cur.execute('UPDATE Users SET owner_admin = ? WHERE id_user = ?', (None, id_user_admin))
                    cur.execute('UPDATE Users SET admin_company = ? WHERE id_user = ?', (None, id_user_admin))
                    cur.execute('UPDATE Users SET admin_shop = ? WHERE id_user = ?', (None, id_user_admin))
                    cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', (None, id_user_admin))
                else:
                    cur.execute('UPDATE Users SET owner_admin = ? WHERE id_user = ?', ('/'.join(owner_admin), id_user_admin))
                    cur.execute('UPDATE Users SET admin_company = ? WHERE id_user = ?', ('/'.join(admin_company), id_user_admin))
                    cur.execute('UPDATE Users SET admin_shop = ? WHERE id_user = ?', ('/'.join(admin_shop), id_user_admin))
                    cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ('/'.join(task_id), id_user_admin))

            count = 0
            all_check = tmp_check_name_shop + tmp_check_id_shop + tmp_check_id_shop + tmp_id_token + tmp_name_company + tmp_permission_user + tmp_time_add + tmp_pull_add + tmp_id_admin + tmp_task_id

            for i in range(len(all_check)):
                if len(all_check[i]) > 0:
                    count += 1

            if count == len(all_check):
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(tmp_check_name_shop), id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', ('/'.join(tmp_check_id_shop), id_user))
                cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?',('/'.join(tmp_time_add), id_user))
                cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ('/'.join(tmp_pull_add), id_user))
                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', ('/'.join(tmp_check_token), id_user))
                cur.execute('UPDATE Users SET id_token= ? WHERE id_user = ?', ('/'.join(tmp_id_token), id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', ('/'.join(tmp_name_company), id_user))
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', ('/'.join(tmp_permission_user), id_user))
                cur.execute('UPDATE Users SET id_admin = ? WHERE id_user = ?', ('/'.join(tmp_id_admin), id_user))
                cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', ('/'.join(tmp_task_id), id_user_admin))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                con.commit()
                return text_msg[0]

            elif count < len(all_check):
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET id_token= ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET id_admin = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET task_id = ? WHERE id_user = ?', (None, id_user_admin))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                con.commit()
                return text_msg[0]

        con.commit()
        return text_msg[1]