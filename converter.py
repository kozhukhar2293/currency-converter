 # converter.py
 # Файл для конвертации валют
import requests
import os
import time
import json

# Константы
URL_API = 'https://open.er-api.com/v6/latest/USD'
CACHE_FILE = 'rates_cache.json' # кэш в котором хранятся курсы валют, обновляется каждый час
CACHE_DURATION = 60 # время жизни файла до обновления

def get_rates() -> dict:
    '''Возвращает словарь с курсами валют относительно USD'''
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cached_data = f.read()
                # Превращаем строку обратно в словарь
                cached = json.load(f)

                # Проверяем не устарел ли кэш
                age = time.time - cached['timestamp']
                if age < CACHE_DURATION:
                    print('Использую кэш, курсы валют свежие')
                    return cached['rates']
                else:
                    print('Кэш устарел, обновляю курсы валют...')    
        except Exception:
            # Если что-то пошло не так, игнорируем и идем в API
            pass       
    # Если кэша нет или он устарел, идем в API         
    print('Запрашиваю данные из API...')    
    response = requests.get(URL_API, timeout=10) # Получаем ответ
    response.raise_for_status() # Получаем статус
    data = response.json()

    if data.get('result') != 'success': # Проверка на ошибку
        raise RuntimeError('API вернул ошибку')
    rates = data['rates']
    # Сохраняем в кэш
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({"timestamp": time.time(), "rates": rates}, f)
        print('Курсы сохранены в файл')
    except Exception as e:
        # Если не удалось сохранить кэш, предупреждаем
        print(f'Не удалось сохранить кэш {e}')        
    return rates
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

