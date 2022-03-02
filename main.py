import xml.dom.minidom as minidom
from pprint import pprint


def main():
    dom = minidom.parse('RS_Via-3.xml')
    dom.normalize()

    elements = dom.getElementsByTagName("Flight")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Carrier':
                    if child.firstChild.nodeType == 3:
                        currency_dict['Carrier'] = child.firstChild.data
                if child.tagName == 'FlightNumber':
                    if child.firstChild.nodeType == 3:
                        currency_dict['Flight Number'] = child.firstChild.data
        pprint(currency_dict)


if __name__ == '__main__':
    main()
