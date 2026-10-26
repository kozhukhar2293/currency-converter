 # core.py
import requests
import json
import os
import time

URL_API = 'https://open.er-api.com/v6/latest/USD'
CACHE_FILE = 'rates_cache.json' # кэш в котором хранятся курсы валют, обновляется каждый час
CACHE_DURATION = 3600 # время жизни файла до обновления

def get_rates() -> dict:
    '''Возвращает словарь с курсами валют относительно USD'''
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                # Превращаем строку обратно в словарь
                cached = json.load(f)

                # Проверяем не устарел ли кэш
                age = time.time() - cached['timestamp']
                if age < CACHE_DURATION:
                    print('Использую кэш, курсы валют свежие')
                    return cached['rates']
                else:
                    print('Кэш устарел, обновляю курсы валют...')   
        except Exception:
            # Если что-то пошло не так, игнорируем и идем в API
            pass       
    # Запрос в API     
    print('Запрашиваю данные из API...')    
    try:
        response = requests.get(URL_API, timeout=10) # Получаем ответ
        response.raise_for_status() # Получаем статус
    except requests.exceptions.RequestException as e: # Если сайт упал или проблемы с интернетом
        raise RuntimeError(f'Ошибка в сети {e}')
    try:
        data = response.json()
    except json.JSONDecodeError: # Может произойти ситуация когда отправленно все верно, но в неправильном формате(HTML)
        raise RuntimeError('API вернул не JSON')

    if data.get('result') != 'success': # Проверка на ошибку
        raise RuntimeError('API вернул ошибку')
    rates = data['rates']
    # Сохраняем в кэш
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({"timestamp": time.time(), "rates": rates}, f)
        print('Курсы сохранены в файл')
    except Exception as e:
        # Если не удалось сохранить кэш
        print(f'Не удалось сохранить кэш {e}')    

    # Возвращаем      
    return rates

def convert(amount: float, from_cur: str, to_cur: str, rates: dict) -> float: 
    '''Функция для конвертирования валюты через курс USD'''
    amount_usd = amount / rates[from_cur]
    return amount_usd * rates[to_cur]