import os

from aiogram import F, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram.types import Message, InputFile, FSInputFile

from API_WB import edit_qr
from DATA_BASE import db
from LOGIC import kb, text, config

dp = Dispatcher()

db_process = db.options_db()

@dp.message(Command(config.commands[0][1:])) #/start
async def start_handler(msg: Message):
    text_msg = db_process.add_user(msg.from_user.id, msg.chat.username, config.statuses[0], text.start_text_2[2])
    await msg.answer(text_msg[1], reply_markup=kb.start_2)

@dp.message(Command(config.commands[1][1:])) #/menu
async def menu_handler(msg: Message):
    if db_process.create_tuple_db_posizione(msg.from_user.id, config.name_posizione[14])[0] == 'admin':
        text_msg = db_process.change_status(msg.from_user.id, config.statuses[0], text.reg_admin, 'st_b')
        await msg.answer(text_msg, reply_markup=kb.create_access_shop_buttons(msg.from_user.id))

    elif db_process.create_tuple_db_posizione(msg.from_user.id, config.name_posizione[14])[0] == 'owner':
        text_msg = db_process.change_status(msg.from_user.id, config.statuses[0], text.start_text, 'st_b')
        await msg.answer(text_msg, reply_markup=kb.start)

@dp.message()
async def add(msg: Message): #действия
    text_msg = text.start_text[1]
    flag = 0

    if db_process.check_status(msg.from_user.id, config.statuses[2]) and (msg.text not in config.commands): #добавление токена
        text_msg = db_process.add_token(msg.from_user.id, msg.text, text.add_token)

    if db_process.check_status(msg.from_user.id, config.statuses[1]) and (msg.text not in config.commands): #добавление магазина
        text_msg = db_process.add_shop(msg.from_user.id, msg.text, text.change_status)

    elif db_process.check_status(msg.from_user.id, config.statuses[4]) and (msg.text not in config.commands): #добавление админа
        text_msg = text.add_admin[2]
        if msg.forward_from != None:
            text_msg = db_process.add_admin(msg.from_user.id, str(msg.forward_from.id), text.admin, str(msg.forward_from.username))

    elif db_process.check_status(msg.from_user.id, config.statuses[11]) and (msg.text not in config.commands): #изменение названия магазина
        text_msg = db_process.change_name_shop(msg.from_user.id, msg.text)

    elif db_process.check_status(msg.from_user.id, config.statuses[7]) and (msg.text not in config.commands): #добавление времени запуска/остановки рекламы
        text_msg = db_process.add_time(msg.from_user.id, msg.text, text.check_time)[0]
        flag = db_process.add_time(msg.from_user.id, msg.text, text.check_time)[1]

    elif db_process.check_status(msg.from_user.id, config.statuses[15]) and (msg.text not in config.commands): #ввод данных для парссинга позиций
        text_msg = await db_process.ret_pozitione(msg.text, msg.from_user.id)

    elif db_process.check_status(msg.from_user.id, config.statuses[10]) and (msg.text not in config.commands): #ввод данных для фиксирования фраз
        text_msg = db_process.key_query(msg.from_user.id, msg.text, text.key_query_2)

    elif db_process.check_status(msg.from_user.id, config.statuses[14]) and (msg.text not in config.commands): #ввод данных для qr
        text_msg = edit_qr.edit_qr_conde_image(msg.chat.id, msg.text, text.gen_QR_2)[0]

    if text_msg == text.check_time[1]:
        await msg.answer(text_msg)

    elif text_msg == text.gen_QR_2[0]:
        path = edit_qr.edit_qr_conde_image(msg.from_user.id, msg.text, text.gen_QR_2)[1]
        if db_process.create_tuple_db_posizione(msg.from_user.id, config.name_posizione[14])[0] == 'admin':
            await msg.answer_document(document=FSInputFile(path), caption=text.gen_QR_2[0])
            os.remove(path)

        await msg.answer_document(document=FSInputFile(path), caption=text.gen_QR_2[0])
        os.remove(path)

    elif text_msg == text.change_status[0]:
        await msg.answer(text_msg, reply_markup=kb.cancellation, parse_mode="HTML")

    elif flag == 1:
        await msg.answer(text_msg, reply_markup=kb.menu_admin)

    else:
        await msg.answer(text_msg, reply_markup=kb.menu, parse_mode="HTML")

@dp.callback_query(F.data == 'reg_owner') #выбор владельца
async def reg_owner(call: CallbackQuery):
    type_user = call.data.replace('reg_', '')
    text_msg = db_process.reg_user(call.message.chat.id, type_user, text.start_text)
    await call.message.edit_text(text_msg, reply_markup=kb.start)

@dp.callback_query(F.data == 'reg_admin') #выбор админа
async def reg_admin(call: CallbackQuery):
    type_user = call.data.replace('reg_', '')
    text_msg = db_process.reg_admin(call.message.chat.id, type_user, text.reg_admin)
    await call.message.edit_text(text_msg, reply_markup=kb.create_access_shop_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'change_mode') #выбор режима
async def change_mode(call: CallbackQuery):
    text_msg = text.start_text_2[2]
    await call.message.edit_text(text_msg, reply_markup=kb.start_2)

@dp.callback_query(F.data == 'cancellation') #отмена токена
async def cancellation_token(call: CallbackQuery):
    text_msg = db_process.cancellation_token(call.message.chat.id, text.cancellation_token)
    await call.message.edit_text(text_msg, reply_markup=kb.start)

@dp.callback_query(F.data == 'add_shop') #добавить магазин
async def request_add_shop(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[1], text.add_shop, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'list_shop') #список магазинов кнопками
async def shop_list(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[0], text.set_shop, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_shop_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'add_admin') #добавить админа
async def request_add_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[4], text.add_admin, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'del_admin') #удалить админа
async def request_del_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[5], text.del_admin, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_admin_buttons(call.message.chat.id))

@dp.callback_query(F.data.startswith('use_adm-')) #выбор админа
async def work_with_admin(call: CallbackQuery):
    use_adm_name = call.data.replace('use_adm-', '')
    text_msg = db_process.del_admin(call.message.chat.id, text.admin_delete, use_adm_name)
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data.startswith('dt_sh-')) #выбор магазина
async def work_with_shop(call: CallbackQuery):
    dt_sh_name = call.data.replace('dt_sh-', '')
    text_msg = db_process.change_status(call.message.chat.id, dt_sh_name, text.in_shop, 'st_sh')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_company_buttons(call.message.chat.id))

@dp.callback_query(F.data.startswith('dt_cp-')) #выбор компании
async def work_with_company(call: CallbackQuery):
    dt_sh_name = call.data.replace('dt_cp-', '')
    text_msg = db_process.change_status(call.message.chat.id, dt_sh_name, text.text_info_company(call.message.chat.id, dt_sh_name), 'st_cp')
    await call.message.edit_text(text_msg, reply_markup=kb.create_in_company_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'change_name') #изменение названия магазина
async def change_name_shop(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[11], text.change_name, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'full_time') #работа с настройками времени
async def work_with_time_add(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[00], text.full_time, 'st_b')
    use_company = db_process.ret_use_company(call.message.chat.id)
    status_add = text.check_status(call.message.chat.id, use_company)
    if status_add == 'приостановлено':
        await call.message.edit_text(text_msg, reply_markup=kb.time)
    elif status_add == 'запущено':
        await call.message.edit_text(text_msg, reply_markup=kb.time_2)

@dp.callback_query(F.data == 'time_start_add') #добавление времени запуска/остановки рекламы
async def time_add(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[7], text.time_add, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'key_query') #обработка выбора фиксирования ключевых фраз
async def key_query(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[10], text.key_query, 'st_b')
    if db_process.create_tuple_db_posizione(call.message.chat.id, config.name_posizione[14])[0] == 'admin':
        await call.message.edit_text(text_msg, reply_markup=kb.menu_admin)

    elif db_process.create_tuple_db_posizione(call.message.chat.id, config.name_posizione[14])[0] == 'owner':
        await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'del_time_start_add') #выбор для удаления времени запуска/остановки рекламы
async def del_time_add(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[13], text.del_time, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_time_buttons(call.message.chat.id))

@dp.callback_query(F.data.startswith('dl_time-')) #удаление времени запуска/остановки рекламы
async def del_time_add_2(call: CallbackQuery):
    dt_sh_name = call.data.replace('dl_time-', '')
    text_msg = db_process.del_time(call.message.chat.id, dt_sh_name, text.delete_time)
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_time_buttons(call.message.chat.id))

@dp.callback_query(F.data.startswith('dl_admin-')) #выбор админа для удаления
async def del_admin(call: CallbackQuery):
    dt_sh_name = call.data.replace('dl_admin-', '')
    text_msg = db_process.del_admin(call.message.chat.id, text.admin_delete, dt_sh_name)
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'start_add') #ручной запуск рекламы
async def start_add(call: CallbackQuery):
    text_msg = db_process.start_add(call.message.chat.id)
    await call.message.edit_text(text_msg, reply_markup=kb.time_2)

@dp.callback_query(F.data == 'stop_add') #ручная остановка рекламы
async def start_add(call: CallbackQuery):
    text_msg = db_process.stop_add(call.message.chat.id)
    await call.message.edit_text(text_msg, reply_markup=kb.time)

@dp.callback_query(F.data == 'del_shop') #удаление магазина
async def del_shop(call: CallbackQuery):
    text_msg = db_process.del_shop(call.message.chat.id, text.del_shop)
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_del_shop_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'main_menu') #вернуться в главное меню
async def main_menu(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[0], text.start_text, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.start)

#ФУНКЦИИ АДМИНА

@dp.callback_query(F.data == 'update_shop_admin') #обновление магазинов админа
async def update_shop(call: CallbackQuery):
    type_user = call.data.replace('update_shop_', '')
    text_msg = db_process.reg_admin(call.message.chat.id, type_user, text.reg_admin_update)
    await call.message.edit_text(text_msg, reply_markup=kb.create_access_shop_buttons_2(call.message.chat.id))

@dp.callback_query(F.data.startswith('dt_sh_admin-')) #выбор магазина админом
async def work_with_shop_admin(call: CallbackQuery):
    dt_sh_name = call.data.replace('dt_sh_admin-', '')
    text_msg = db_process.change_status(call.message.chat.id, dt_sh_name, text.in_company, 'st_sh')
    await call.message.edit_text(text_msg, reply_markup=kb.create_access_company_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'update_admin') #обновление компаний админа
async def update_company(call: CallbackQuery):
    type_user = call.data.replace('update_', '')
    text_msg = db_process.reg_admin(call.message.chat.id, type_user, text.reg_admin_update_cp)
    await call.message.edit_text(text_msg, reply_markup=kb.create_access_company_buttons_2(call.message.chat.id))

@dp.callback_query(F.data.startswith('dt_cp_admin-')) #выбор компании админом
async def work_with_company_admin(call: CallbackQuery):
    dt_sh_name = call.data.replace('dt_cp_admin-', '')
    text_msg = db_process.change_status(call.message.chat.id, dt_sh_name, text.in_company, 'st_cp')
    await call.message.edit_text(text_msg, reply_markup=kb.in_company_admin_kb)

@dp.callback_query(F.data == 'full_time_admin') #работа с настройками времени админом
async def work_with_time_add_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[00], text.full_time, 'st_b')
    use_company = db_process.ret_use_company(call.message.chat.id)
    status_add = text.check_status(call.message.chat.id, use_company)
    if status_add == 'приостановлено':
        await call.message.edit_text(text_msg, reply_markup=kb.time_admin)
    elif status_add == 'запущено':
        await call.message.edit_text(text_msg, reply_markup=kb.time_admin_2)


@dp.callback_query(F.data == 'time_start_add_admin') #добавление времени запуска/остановки рекламы админом
async def time_add_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[7], text.time_add, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu_admin)

@dp.callback_query(F.data == 'del_time_start_add_admin') #выбор для удаления времени запуска/остановки рекламы
async def del_time_add_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[13], text.del_time, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_time_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'main_menu_admin') #вернуться в главное меню
async def main_menu_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[0], text.reg_admin, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.create_access_shop_buttons(call.message.chat.id))

#ОБЩИЕ ФУНКЦИИ

@dp.callback_query(F.data == 'gen_QR') #ввод данных для генерации QR
async def gen_QR(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[14], text.gen_QR, 'st_b')
    if db_process.create_tuple_db_posizione(call.message.chat.id, config.name_posizione[14])[0] == 'admin':
        await call.message.edit_text(text_msg, reply_markup=kb.menu_admin)

    elif db_process.create_tuple_db_posizione(call.message.chat.id, config.name_posizione[14])[0] == 'owner':
        await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'check_pozitione') #ввод данных для определения позиций
async def check_pozitione(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[15], text.check_pozitione, 'st_b')
    if db_process.create_tuple_db_posizione(call.message.chat.id, config.name_posizione[14])[0] == 'admin':
        await call.message.edit_text(text_msg, reply_markup=kb.menu_admin)

    elif db_process.create_tuple_db_posizione(call.message.chat.id, config.name_posizione[14])[0] == 'owner':
        await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'manual') #инструкция
async def manual(call: CallbackQuery):
    text_msg = text.manual[0]
    await call.message.edit_text(text_msg, reply_markup=kb.manual_kb, parse_mode="HTML")