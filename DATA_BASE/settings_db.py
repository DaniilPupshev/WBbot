import sqlite3
import uuid

#тут просто сбрасываю флаг в бд
connection = sqlite3.connect('../database.db')
cursor = connection.cursor()
# cursor.execute('DELETE FROM Users WHERE status_bot = ?', ('waiting',))
# # cursor.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', 956854913))
# connection.commit()
# connection.close()

# Создаем подключение к базе данных (файл database.db будет создан)
# connection = sqlite3.connect('database.db')
# cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id_user INTEGER PRIMARY KEY,
owner_nick TEXT,
status_bot TEXT,
id_shop TEXT,
id_admin TEXT,
name_shop TEXT,
token TEXT,
permission_user TEXT,
time_add TEXT,
use_shop TEXT,
id_token TEXT,
pull_add TEXT,
name_company TEXT,
use_company TEXT,
type_user TEXT,
admin_company TEXT,
owner_admin TEXT,
admin_shop TEXT,
task_id TEXT
)
''')

# # Создаем индекс для столбца "nick_user"
# cursor.execute('CREATE INDEX idx_nick_user ON Users (nick_user)')

# cursor.execute(
#     'INSERT INTO Users (id_user, nick_user, status_bot) VALUES (?, ?, ?)',
#     (
#         56843e3,
#         'd2uvrw',
#         'qqq',
#     )
# )

#добавление данных (можно использовать REPLACE вместо INSERT, чтобы избежать ошибок в совпадении данных)

#изменение данных
# cursor.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', 956854913))

#удаление данных
# cursor.execute('DELETE FROM Users WHERE status_bot = ?', ('waiting',))

# Выбираем всех пользователей
# cursor.execute('SELECT * FROM Users')
# users = cursor.fetchall()

# # Выводим результаты в формате: (6485832, 'ivan@qqq', 'waiting', None, None, None, None, None, None)
# for user in users:
#   print(user)

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()