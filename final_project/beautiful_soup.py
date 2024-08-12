from bs4 import BeautifulSoup as BS
import urllib.request as libreq
import urllib.parse as libparse
import re


CHARLIMIT = 10_000_000
AGENCIESPATH = "C:\\Github\\Learning\\final_project\\agencies\\"


class Pattern:
        """
        Primarily stores useful Regex patterns 
        """
        # Searches for 'propertyCards'
        p1 = r"propertyCard-(\w+)\W" 
        # Searches for 'propertyCard'-related image urls
        p2 = r"<img alt=\"Property Image \d?\d\" itemprop=\"image\" src=\"(.+)\""
        # Captures a relevant 'path' for a URL 
        p3 = r"<a class=\"propertyCard-additionalImgs\" href=\"(.+?)\""
        # UK URL pattern, captures: 1) 'Origin' of url [Ignores last '/'], 2) Domain of URL 
        p4 = r"(https:\/\/(?:www.)?(.+?)(?:(?:\.co|\.org).uk|\.com))\/"
        # urllib.request headings -- a.k.a. (some) class attributes and methods
        p5 = r"title=\"urllib\.request\.(.*?)\""

class Webpage:
    def __init__(self):
        # 'Origin' attribute
        # 'TLD' attribute
        # 'Path' attribute
        # Query formatting as func of domain name
        #   i.e. rightmovepage.qprotocol(user values) -> rightmovepath / full rightmove url  
        #     or just handle qprotocol separately, considering it'll just be domain dependent.
        ...



def url_in_list(input_url: str) -> bool:
    """
    Checks whether provided url has matching 'domain' and 'TLD' with those
    documented in 'final_project/agencies/agencies.txt'
    Change these variable names!
    """
    if not input_url:
        raise ValueError("url_in_list: No input entered")
    
    # Matches origin of input_url, if valid
    if search := re.search(Pattern.p4, input_url):
        input_origin = search.group(1)
    else:
        raise ValueError("url_in_list: Input URL does not fit expected pattern")
    
    # Check if origin of URLs in each row of agencies.txt matches input_origin 
    with open(AGENCIESPATH + "agencies.txt", 'r') as file:
        for row in file:
            if row_origin := re.search(Pattern.p4, row).group(1) == input_origin:
                return True
    return False


def url_to_txt(url: str, dest:str) -> None:
    with libreq.urlopen(url) as url:
        doc = url.read(CHARLIMIT)
    prettified = BS(doc, 'html.parser').prettify()
    with open(dest, 'w') as file:
        for row in prettified:
            file.write(row)


def parse_file_to_BS(filename: str) -> BS:
    """
    Takes in a filename in 'filename.html' format
    Outputs the BS (BeautifulSoup) object, parsed in 'html'
        Read-only, encoded in utf-8
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return BS(file, 'html.parser')
    

def matches_to_txt(input_file: str, output_file: str, pattern: str, *catches: list) -> None:
    """
    Searches for `pattern` matches in `input_file`, outputs matches to `output_file`
    Want to add functionality for which 'groups' of the match object to capture
    """
    try:
        attr_pattern = getattr(Pattern, pattern)
    except AttributeError:
        raise AttributeError("Invalid pattern choice")
    
    matches = []
    with open(input_file, 'r') as file:
        for line in file:
            matches.append(re.search(attr_pattern, line))
    list_matches = []
    ## EDIT SUGGESTION ## Could probably join these loops together
    for match in matches:
        if match and match.group(1) not in list_matches:
            list_matches.append(match.group(1))
    with open(output_file, 'w') as newfile:
        for match in list_matches:
            newfile.write(match + '\n')


def rightmove_query_parser():
    """
    Takes info from rightmove/sample_urls.txt and makes dictionary of unique query terms

    Could strip the information before the query from the URL to save storage but cba with that yet
    """
    unique_qs = {}
    with open(AGENCIESPATH+'rightmove/sample_urls.txt', 'r') as file:
        for row in file:
            url_queries_string = libparse.urlparse(row)[4]
            query_dict = libparse.parse_qs(url_queries_string)
            for query in query_dict:
                if query in unique_qs:
                    for item in query_dict[query]:
                        if item not in unique_qs[query]:
                            unique_qs[query].append(item)
                else:
                    unique_qs[query] = query_dict[query]

    with open(AGENCIESPATH+'rightmove/query_terms.txt', 'w') as file:
        for index, query in enumerate(unique_qs, start=1):
            file.write(f"#{index}: {query} = {unique_qs[query]}\n" )


def main():
    rightmove_query_parser()

if __name__ == "__main__":
    main()