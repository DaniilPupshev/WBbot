import requests
import itertools
import json

import asyncio
import time
from aiogram import Bot
from aiogram.client.session import aiohttp

from LOGIC import config

bot = Bot(token=config.BOT_TOKEN)

class work_api():
    def __init__(self):
        self.type_ping = [
            'https://content-api.wildberries.ru/ping',
            'https://seller-analytics-api.wildberries.ru/ping',
            'https://discounts-prices-api.wildberries.ru/ping',
            'https://marketplace-api.wildberries.ru/ping',
            'https://statistics-api.wildberries.ru/ping',
            'https://advert-api.wildberries.ru/ping',
            'https://feedbacks-api.wildberries.ru/ping',
            'https://buyer-chat-api.wildberries.ru/ping',
            'https://supplies-api.wildberries.ru/ping',
            'https://returns-api.wildberries.ru/ping',
            'https://documents-api.wildberries.ru/ping',
            'https://common-api.wildberries.ru/ping',
        ]

    def check_token(self, token):
        count = 0
        for check_type_ping in self.type_ping:
            url = check_type_ping

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                count += 1

        # if count == len(self.type_ping): #Узнать на что должны быть права
        if count == 5:
            return True
        return False

    def get_list_campaign(self, token, status, type):
        url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'status': status,
            'type': type,
            'order': "create",
            'direction': "desc"
        }

        response = requests.post(url, headers=headers, params=params)
        return response

    def get_full_list_campaign(self, token):
        response = self.get_list_campaign(token, 11, 8)
        list_campaign_11_8 = []
        if response.status_code == 200:
            list_campaign_11_8 = [[i['name'], i['advertId']] for i in response.json()]

        response = self.get_list_campaign(token, 9, 8)
        list_campaign_9_8 = []
        if response.status_code == 200:
            list_campaign_9_8 = [[i['name'], i['advertId']] for i in response.json()]

        response = self.get_list_campaign(token, 11, 9)
        list_campaign_11_9 = []
        if response.status_code == 200:
            list_campaign_11_9 = [[i['name'], i['advertId']] for i in response.json()]

        response = self.get_list_campaign(token, 9, 9)
        list_campaign_9_9 = []
        if response.status_code == 200:
            list_campaign_9_9 = [[i['name'], i['advertId']] for i in response.json()]

        list_campaign = list_campaign_11_8 + list_campaign_9_8 + list_campaign_11_9 + list_campaign_9_9
        return list_campaign

    def start_campaign(self, token, id_campaign):
        url = 'https://advert-api.wb.ru/adv/v0/start'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'id': id_campaign,
        }

        response = requests.get(url, headers=headers, params=params)
        return response

    def pause_campaign(self, token, id_campaign):
        url = 'https://advert-api.wb.ru/adv/v0/pause'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'id': id_campaign,
        }

        response = requests.get(url, headers=headers, params=params)
        return response

    def get_info_campaign(self, token, id_campaign):
        id_campaign = str(id_campaign)

        response_11_8 = self.get_list_campaign(token, 11, 8)

        response_9_8 = self.get_list_campaign(token, 9, 8)

        response_11_9 = self.get_list_campaign(token, 11, 9)

        response_9_9 = self.get_list_campaign(token, 9, 9)

        data_11_8 = response_11_8.json() if response_11_8.content else []
        data_9_8 = response_9_8.json() if response_9_8.content else []
        data_11_9 = response_11_9.json() if response_11_9.content else []
        data_9_9 = response_9_9.json() if response_9_9.content else []

        if isinstance(data_11_8, dict):
            data_11_8 = [data_11_8]
        if isinstance(data_9_8, dict):
            data_9_8 = [data_9_8]
        if isinstance(data_11_9, dict):
            data_11_9 = [data_11_9]
        if isinstance(data_9_9, dict):
            data_9_9 = [data_9_9]

        response = data_11_8 + data_9_8 + data_11_9 + data_9_9

        flag = False
        for item in response:
            if 'advertId' in item and str(item['advertId']) == str(id_campaign):
                flag = True
                break

        if flag:
            return item
        return {}

    def budget_campaign(self, token, id_campaign):
        url = 'https://advert-api.wb.ru/adv/v1/budget'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'id': id_campaign,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()['total']
        return ''

    async def start_campaign1(self, wb_token, id_campaign, id_user):
        response = self.start_campaign(wb_token, id_campaign)

        if response.status_code == 200:
            text_msg = f'Компания {id_campaign} запущена'
        else:
            text_msg = 'Ошибка'

        await bot.send_message(id_user, text_msg)

    async def pause_campaign1(self, wb_token, id_campaign, id_user):
        response = self.pause_campaign(wb_token, id_campaign)

        if response.status_code == 200:
            text_msg = f'Компания {id_campaign} остановлена'
        else:
            text_msg = 'Ошибка'

        await bot.send_message(id_user, text_msg)

# class WildBerriesParser:
#     def __init__(self, key_word):
#         self.key_word = key_word
#         self.headers = {
#             'Accept': "*/*",
#             'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"
#         }
#         self.product_cards = []
#
#     def get_products_on_page(self, page_data: dict) -> list:
#         products_on_page = []
#
#         try:
#             for item in page_data['data']['products']:
#                 products_on_page.append({
#                     'Ссылка': f"https://www.wildberries.ru/catalog/"
#                               f"{item['id']}/detail.aspx",
#                     'Артикул': item['id'],
#                     'Наименование': item['name'],
#                     'Бренд': item['brand'],
#                     'ID бренда': item['brandId'],
#                     'Цена': int(item['priceU'] / 100),
#                     'Цена со скидкой': int(item['salePriceU'] / 100),
#                     'Рейтинг': item['rating'],
#                     'Отзывы': item['feedbacks']
#                 })
#         except:
#             pass
#
#         return products_on_page
#
#     def add_data_from_page(self, url: str):
#         response = requests.get(url, headers=self.headers).json()
#         page_data = self.get_products_on_page(response)
#
#         if len(page_data) > 0:
#             self.product_cards.extend(page_data)
#             # print(f"Добавлено товаров: {len(page_data)}")
#         else:
#             # print('Загрузка товаров завершена')
#             return True
#
#     def get_all_products_in_search_result(self, key_word: str):
#         for page in range(1, 101):
#             # print(f"Загружаю товары со страницы {page}")
#             url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?"
#                    f"appType=1&curr=rub&dest=-1257786&page={page}"
#                    f"&query={'%20'.join(key_word.split())}&resultset=catalog"
#                    f"&sort=popular&spp=24&suppressSpellcheck=false")
#
#             if self.add_data_from_page(url):
#                 break
#
#     def run_parser(self):
#         self.get_all_products_in_search_result(self.key_word)

class WildBerriesParser:
    def __init__(self, key_word):
        self.key_word = key_word
        self.headers = {
            'Accept': "*/*",
            'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"
        }
        self.product_cards = []

    async def get_products_on_page(self, page_data: dict) -> list:
        products_on_page = []

        try:
            for item in page_data['data']['products']:
                products_on_page.append({
                    'Ссылка': f"https://www.wildberries.ru/catalog/"
                              f"{item['id']}/detail.aspx",
                    'Артикул': item['id'],
                    'Наименование': item['name'],
                    'Бренд': item['brand'],
                    'ID бренда': item['brandId'],
                    'Цена': int(item['priceU'] / 100),
                    'Цена со скидкой': int(item['salePriceU'] / 100),
                    'Рейтинг': item['rating'],
                    'Отзывы': item['feedbacks']
                })
        except Exception as e:
            print(f"Ошибка при обработке страницы: {e}")

        return products_on_page

    async def add_data_from_page(self, url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        # Принудительное декодирование как JSON
                        try:
                            page_data = await response.json(content_type=None)
                        except Exception as e:
                            print(f"Ошибка при декодировании JSON: {e}")
                            return True  # Завершаем парсинг

                        # Проверяем структуру данных
                        if 'data' in page_data and 'products' in page_data['data']:
                            products = page_data['data']['products']
                            if not products:
                                # Если товаров нет, завершаем парсинг
                                return True

                            # Парсим товары и добавляем их в список
                            page_products = await self.get_products_on_page(page_data)
                            self.product_cards.extend(page_products)
                            return False  # Продолжаем парсинг
                        else:
                            print("Структура данных не соответствует ожидаемой.")
                            return True  # Завершаем парсинг
                    else:
                        print(f"Ошибка при запросе: {response.status}")
                        return True  # Завершаем парсинг
            except Exception as e:
                print(f"Ошибка при выполнении запроса: {e}")
                return True  # Завершаем парсинг

    async def get_all_products_in_search_result(self, key_word: str):
        for page in range(1, 101):
            # print(f"Загружаю товары со страницы {page}")
            url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?"
                   f"appType=1&curr=rub&dest=-1257786&page={page}"
                   f"&query={'%20'.join(key_word.split())}&resultset=catalog"
                   f"&sort=popular&spp=24&suppressSpellcheck=false")

            if await self.add_data_from_page(url):
                break

    async def run_parser(self):
        await self.get_all_products_in_search_result(self.key_word)

async def start(target_artikul, key_word):

    app = WildBerriesParser(key_word)

    await app.run_parser()

    data = app.product_cards

    position = next(
        (i for i, item in enumerate(data) if str(item['Артикул']) == str(target_artikul)),
        None
    )

    return position


# def start(target_artikul, key_word):
#     app = WildBerriesParser(key_word)
#     app.run_parser()
#
#     data = app.product_cards
#     position = next((i for i, item in enumerate(data) if str(item['Артикул']) == str(target_artikul)), None)
#
#     return position

# Функиця получения статистики автоматической кампании по кластерам фраз
def get_words_info(token, id_campaign):
    url = 'https://advert-api.wildberries.ru/adv/v2/auto/stat-words'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    params = {
        'id': id_campaign,
    }

    response = requests.get(url, headers=headers, params=params)
    return response


# Функция для установки стоп кластеров
def set_negative_keywords(token, id_campaign, excluded):
    url = 'https://advert-api.wildberries.ru/adv/v1/auto/set-excluded'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    params = {
        'id': id_campaign,
    }
    data = {
        'excluded': excluded,
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    return response


# Функция для генерации всех перестановок слов в каждой фразе с приведением к нижнему регистру
def generate_permutations(phrases):
    all_permutations = []

    for phrase in phrases:
        words = phrase.lower().split()  # Приводим фразу к нижнему регистру и разделяем на слова
        permutations = itertools.permutations(words)  # Генерируем все перестановки
        # Добавляем все перестановки в общий список
        all_permutations.extend([' '.join(p) for p in permutations])

    return all_permutations


# Функция для получения списка кластеров, в которых есть интересующие фразы
def get_clusters_without_match(clusters, all_permuted_phrases):
    # Список кластеров, которые удовлетворяют условию
    clusters_without_match = []

    for cluster in clusters:
        # Приводим все ключевые слова к нижнему регистру
        keywords_lower = [keyword.lower() for keyword in cluster['keywords']]

        # Проверяем, что ни одно из ключевых слов не совпадает с любым элементом из all_permuted_phrases
        match_found = any(keyword in all_permuted_phrases for keyword in keywords_lower)

        # Если совпадений нет, добавляем кластер в список
        if not match_found:
            clusters_without_match.append(cluster['cluster'])

    return clusters_without_match


#  Функция для установки стоп кластеров по фразам исключениям в конкретной рекламной компании
def set_negative_keywords_without_match(wb_token, my_phrases, id_campaign):
    # Получение списка кластров с ключевыми запросами и исключениями
    response = get_words_info(wb_token, id_campaign)

    # Преобразование JSON и разбитие на исключения/кластеры
    data = json.loads(response.text)
    excluded = data["excluded"]
    clusters = data["clusters"]

    #     # Пример вывода всех исключений
    #     print("Excluded items:")
    #     for item in excluded:
    #         print(item)

    #     # Пример вывода информации о кластерах
    #     print("\nClusters:")
    #     for cluster in clusters:
    #         print(f"Cluster: {cluster['cluster']}, Count: {cluster['count']}")
    #         print("Keywords:", ", ".join(cluster['keywords']))

    # Генерация всех перестановок для всех фраз
    all_permuted_phrases = generate_permutations(my_phrases)

    # Получение списка кластеров, в которых есть интересующие фразы
    clusters_without_match = get_clusters_without_match(clusters, all_permuted_phrases)

    # Установка стоп кластеров
    response = set_negative_keywords(wb_token, id_campaign, clusters_without_match + excluded)

    return response.status_code


# my_phrases = [
#     'перчатки мужские зимние',
#     'перчатки мужские кожаные зимние',
#     'перчатки мужские кожаные',
#     'перчатки мужские',
#     'перчатки утепленные',
#     'перчатки кожаные'
# ]