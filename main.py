import argparse
import xml.dom.minidom as minidom

from datetime import datetime
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
        help='Самая дорогая стоимость перелета',
    )
    parser.add_argument(
        '--min_price',
        action="store_true",
        help='Самая низкая стоимость перелета',
    )
    return parser


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
                if child.tagName == 'DepartureTimeStamp':
                    if child.firstChild.nodeType == 3:
                        departure = child.firstChild.data
                if child.tagName == 'ArrivalTimeStamp':
                    if child.firstChild.nodeType == 3:
                        arrival = child.firstChild.data
                        flight['flght_time'] = get_flight_time(
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
    delta = (arrival - departure).total_seconds()
    return delta


def main():
    parser = add_argument_parser()
    args = parser.parse_args()
    flights_1 = get_flights('RS_ViaOW.xml')
    flights_2 = get_flights('RS_Via-3.xml')
    prices_1 = get_price_ticket('RS_ViaOW.xml')
    prices_2 = get_price_ticket('RS_Via-3.xml')

    if args.count:
        print(len(flights_1)+len(flights_2))

    if args.max_price:
        print(max(prices_1 + prices_2))

    if args.min_price:
        print(min(prices_1 + prices_2))


if __name__ == '__main__':
    main()
