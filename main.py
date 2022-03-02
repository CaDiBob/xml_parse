import xml.dom.minidom as minidom

from datetime import datetime
from pprint import pprint



def get_format_date(raw_date):
    date, time = raw_date.split("T")
    processed_date = date +  f'T{time[:2]}:{time[2:]}'
    processed_date = datetime.fromisoformat(processed_date)
    return processed_date


def get_flight_time(departure, arrival):
    departure = get_format_date(departure)
    arrival = get_format_date(arrival)
    delta = (arrival - departure).total_seconds()
    return delta


def main():
    dom = minidom.parse('RS_Via-3.xml')
    dom.normalize()

    elements = dom.getElementsByTagName("Flight")
    flights = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Carrier':
                    if child.firstChild.nodeType == 3:
                        flights['carrier'] = child.firstChild.data
                if child.tagName == 'FlightNumber':
                    if child.firstChild.nodeType == 3:
                        flights['code'] = child.firstChild.data
                if child.tagName == 'DepartureTimeStamp':
                    if child.firstChild.nodeType == 3:
                        departure = child.firstChild.data
                if child.tagName == 'ArrivalTimeStamp':
                    if child.firstChild.nodeType == 3:
                        arrival = child.firstChild.data
                        flights['flght_time'] = get_flight_time(departure, arrival)
        print(flights)


if __name__ == '__main__':
    main()
