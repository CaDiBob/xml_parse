# Скрипт парсит xml

Выводит в консоль данные: Общее количество рейсов, самая высокая стоимость перелета, самая низкая стоимость перелета и билетов туда и обратно


### Как установить
Python3 должен быть установлен. Затем используйте `pip`

```bash
pip install -r requirements.txt
```

### Как запустить

##### Для запуска скрипта введите:

```bash
python main.py
```

#### Принимает на вход аргументы


Общее количество рейсов

```bash
python main.py --count
```

Самая дорогая стоимость перелета

```bash
python main.py --max_price 
```
Самая низкая стоимость перелета

```bash
python main.py --min_price
``` 
Билетов туда и обратно

```bash
python main.py --round_trip
```

Прямые рейсы из Дубая в Бангкок

```bash
python main.py --direct_flights
```