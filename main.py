import argparse
import xml.dom.minidom as minidom

from datetime import datetime
from terminaltables import AsciiTable
from pprint import pprint


def add_argument_parser():
    parser = argparse.ArgumentParser(
        description='Парсит xml файлы и выводит данные по ним'
    )
    parser.add_argument(
        '--count',
        action="store_true",
        help='Общее количество рейсов',
    )
    parser.add_argument(
        '--max_price',
        action="store_true",
        help='Самая высокая стоимость перелета',
    )
    parser.add_argument(
        '--min_price',
        action="store_true",
        help='Самая низкая стоимость перелета',
    )
    parser.add_argument(
        '--round_trip',
        action="store_true",
        help='Билетов туда и обратно',
    )
    parser.add_argument(
        '--direct_flights',
        action="store_true",
        help='Прямые рейсы',
    )
    return parser


def get_table(flights, title):
    table_colums = [
        [
            'Авиакомпания',
            'Номер рейса',
            'Код Аэропорта вылета',
            'Код Аэропорта прилета',
            'Время полета',
        ]
    ]
    for flight in flights:
        direct_flight = list()
        for statistic in flight.values():
            direct_flight.append(statistic)
        table_colums.append(direct_flight)
    table = AsciiTable(table_colums, title)
    return table.table


def get_flights(xml_file):
    flights = list()
    dom = minidom.parse(xml_file)
    dom.normalize()
    elements = dom.getElementsByTagName("Flight")
    for node in elements:
        flight = dict()
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Carrier':
                    if child.firstChild.nodeType == 3:
                        flight['carrier'] = child.firstChild.data
                if child.tagName == 'FlightNumber':
                    if child.firstChild.nodeType == 3:
                        flight['code'] = child.firstChild.data
                if child.tagName == 'Source':
                    if child.firstChild.nodeType == 3:
                        flight['Source'] = child.firstChild.data
                if child.tagName == 'Destination':
                    if child.firstChild.nodeType == 3:
                        flight['Destination'] = child.firstChild.data
                if child.tagName == 'DepartureTimeStamp':
                    if child.firstChild.nodeType == 3:
                        departure = child.firstChild.data
                if child.tagName == 'ArrivalTimeStamp':
                    if child.firstChild.nodeType == 3:
                        arrival = child.firstChild.data
                        flight['flight_time'] = get_flight_time(
                            departure,
                            arrival,
                            )
        flights.append(flight)
    return flights


def get_price_ticket(xml_file):
    prices = list()
    dom = minidom.parse(xml_file)
    dom.normalize()
    elements = dom.getElementsByTagName("Pricing")
    for node in elements:
        price = list()
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'ServiceCharges':
                    if child.firstChild.nodeType == 3:
                        price.append(float(child.firstChild.data))

        prices.append(max(price))
    return prices


def get_format_date(raw_date):
    date, time = raw_date.split("T")
    processed_date = date + f'T{time[:2]}:{time[2:]}'
    processed_date = datetime.fromisoformat(processed_date)
    return processed_date


def get_flight_time(departure, arrival):
    departure = get_format_date(departure)
    arrival = get_format_date(arrival)
    delta = arrival - departure
    normal_time = timedelta_to_hms(delta)   
    return normal_time

def timedelta_to_hms(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f'{hours}ч:{minutes}мин'


def get_direct_flights(flights):
    direct_flights = list()
    for flight in flights:
        if flight['Source'] == 'DXB' and flight['Destination'] == 'BKK':
            direct_flights.append(flight)
    return direct_flights


def main():
    parser = add_argument_parser()
    args = parser.parse_args()
    flights_1 = get_flights('RS_ViaOW.xml')
    flights_2 = get_flights('RS_Via-3.xml')
    prices_1 = get_price_ticket('RS_ViaOW.xml')
    prices_2 = get_price_ticket('RS_Via-3.xml')
    direct_flights_1 = get_direct_flights(flights_1)
    direct_flights_2 = get_direct_flights(flights_2)

    if args.count:
        print('Всего рейсов:', len(flights_1)+len(flights_2))

    if args.max_price:
        print('Максимальная стоимость билета:', max(prices_1 + prices_2))

    if args.min_price:
        print('Минимальная стоимость билета:', min(prices_1 + prices_2))

    if args.round_trip:
        print('Билетов туда и обратно:', len(flights_2))

    if args.direct_flights:
        print(get_table(direct_flights_1, title='Прямые рейсы'))
        print(get_table(direct_flights_2, title='Прямые рейсы'))


if __name__ == '__main__':
    main()
