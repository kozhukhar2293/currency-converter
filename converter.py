 # converter.py
 # Файл для конвертации валют
import requests
import os
import time

# Константы
URL_API = 'https://open.er-api.com/v6/latest/USD'
CACHE_FILE = 'rates_cache.json' # кэш в котором хранятся курсы валют, обновляется каждый час
CACHE_DURATION = 300 # время жизни файла до обновления

def get_rates() -> dict:
    '''Возвращает словарь с курсами валют относительно USD'''
    response = requests.get(URL_API, timeout=10) # Получаем ответ
    response.raise_for_status() # Получаем статус
    data = response.json()

    if data.get('result') != 'success': # Проверка на ошибку
        raise 'API вернул ошибку'
    return data['rates']

def convert(amount: float, from_cur: str, to_cur: str, rates: dict) -> float: 
    '''Функция для конвертирования валюты через курс USD'''
    amount_usd = amount / rates[from_cur]
    return amount_usd * rates[to_cur]

def main():
    print('------------Конвертер валют------------')
    print()
    try: 
        rates = get_rates()
    except Exception as e:
        print(f'Не удалось получить курсы: {e}')
        return
    
    available = sorted(rates.keys())
    print('Доступные валюты', ', '.join(available))

    from_cur = input('Из какой валюты: ').upper().strip()
    to_cur = input('В какую валюту: ').upper().strip()

    try:
        amount = float(input('Сумма:')) # Число введенное пользователем

    except ValueError:
        print('Сумма должна быть числом')
        print('Попробуйте еще раз')
        return
    
    if from_cur not in rates or to_cur not in rates:
        print('Извините, такой валюты нет в списке')
        print('Попробуйте еще раз')
        return
    
    result = convert(amount, from_cur, to_cur, rates)
    print(f'{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}')
while True:
    if __name__ == "__main__":
        main()

    answer = input('Хотите продолжить?(Y/N)').lower()   
    if answer == 'n':
        break  

