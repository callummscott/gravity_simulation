from bs4 import BeautifulSoup as BS
import urllib.request as urlreq

CHARLIMIT = 1_000_000

def main():

    input_url = """
    https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E219&insId=1&radius=10.0&minPrice=&maxPrice=1300&minBedrooms=1&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=
    """
    with urlreq.urlopen(input_url) as file:
        doc = file.read(CHARLIMIT)
    preparsed = BS(doc, 'html.parser').prettify()
    print(preparsed)


def got_file(filename: str) -> BS:
    with open(filename, 'r', encoding='utf-8') as file:
        return BS(file, 'html.parser')


if __name__ == "__main__":
    main()