from bs4 import BeautifulSoup as BS
import urllib.request as urlreq
import sys
import os
import re

CHARLIMIT = 10_000_000
AGENCIESPATH = "C:\\Github\\Learning\\final_project\\agencies"

class Pattern():
        # Searches for 'propertyCards'
        p1 = r"propertyCard-(\w+)\W" 
        # Searches for 'propertyCard'-related image urls
        p2 = r"<img alt=\"Property Image \d?\d\" itemprop=\"image\" src=\"(.+)\""
        # Captures a relevant 'path' for a URL 
        p3 = r"<a class=\"propertyCard-additionalImgs\" href=\"(.+?)\""
        # UK URL pattern, captures: 1) 'Origin' of url [Ignores last '/'], 2) Domain of URL 
        p4 = r"(https:\/\/(?:www.)?(.+?)(?:(?:\.co|\.org).uk|\.com))\/"


def url_in_list(input_url: str) -> bool:
    """
    Checks whether provided url has matching 'domain' and 'TLD' with those
    documented in 'final_project/agencies/agencies.txt'
    Change these variable names!
    """
    if not input_url:
        raise ValueError("url_in_list: No input entered")
    
    if search := re.search(Pattern.p4, input_url):
        input_origin = search.group(1)
    else:
        raise ValueError("url_in_list: Input URL does not fit expected pattern")
    
    # Check if origin of URLs in each row of agencies.txt matches input_origin 
    with open(AGENCIESPATH + "\\agencies.txt", 'r') as file:
        for row in file:
            
            if row_origin := re.search(Pattern.p4, row).group(1) == input_origin:
                return True
    return False


def url_to_txt(url: str, dest:str) -> None:
    with urlreq.urlopen(url) as url:
        doc = url.read(CHARLIMIT)
    prettified = BS(doc, 'html.parser').prettify()
    with open(dest, 'w') as file:
        for row in prettified:
            file.write(row)

def got_file(filename: str) -> BS:
    """
    Takes in a filename in 'filename.html' format
    Outputs the BS (BeautifulSoup) object, parsed in 'html'
        Read-only, encoded in utf-8
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return BS(file, 'html.parser')
    

def pattern_search(filename: str) -> None:
    """
    Searches for keywords in file, outputs to 'keywords_found.txt'
    """
    pattern = Pattern.p3
    matches = []
    with open(filename, 'r') as file:
        for line in file:
            matches.append(re.search(pattern, line))
    list_matches = []
    for match in matches:
        if match and match.group(1) not in list_matches:
            list_matches.append(match.group(1))
    with open('keywords_found.txt', 'w') as newfile:
        for match in list_matches:
            newfile.write("https://www.rightmove.co.uk" + match + '\n')

    

    ...


def main():

    input_url = """
    https://www.openrent.co.uk/properties-to-rent/bristol-bristol?term=Bristol,%20Bristol&area=7&prices_min=300&prices_max=1300&bedrooms_min=1&bedrooms_max=2&acceptNonStudents=true&isLive=true
    """
    print(url_in_list("https://www.bristolpropertycentre.co.uk/search/?instruction_type=Letting&department=Residential"))
    



if __name__ == "__main__":
    main()