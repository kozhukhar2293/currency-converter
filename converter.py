 # converter.py
 # Файл для конвертации валют
import core

def main():
    print('------------Конвертер валют------------')
    print()
    try: 
        rates = core.get_rates()
    except Exception as e:
        print(f'Не удалось получить курсы: {e}')
        return
    
    available = sorted(rates.keys())
    print('Доступные валюты', ', '.join(available))

    from_cur = input('Из какой валюты: ').upper().strip()
    to_cur = input('В какую валюту: ').upper().strip()

    try:
        amount = float(input('Сумма: ')) # Число введенное пользователем

    except ValueError:
        print('Сумма должна быть числом')
        print('Попробуйте еще раз')
        return
    
    if from_cur not in rates or to_cur not in rates:
        print('Извините, такой валюты нет в списке')
        print('Попробуйте еще раз')
        return
    
    result = core.convert(amount, from_cur, to_cur, rates)
    print(f'{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}')

if __name__ == "__main__":    
    while True:
        main()
        answer = input('Хотите продолжить?(Y/N)').lower()   
        if answer == 'n':
            break  

