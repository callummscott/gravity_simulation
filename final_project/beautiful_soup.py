from bs4 import BeautifulSoup as BS
import urllib.request as libreq
import urllib.parse as libparse
import tldextract
import json
import re


CHARLIMIT = 10_000_000
AGENCIESPATH = "C:\\Github\\Learning\\final_project\\agencies\\"


class JSONLoadError(Exception):
    """Custom exception for JSON loading errors."""
    pass


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


class HTML:
    def __init__(self):
        ...

class URL:
    def __init__(self):
        super().__init__()

        self.full = ...           #'Origin' attribute
        self.tld = ...              # 'TLD' attribute
        self.path = ...             # 'Path' attribute
        self.query_protocol = ...   # Query formatting as func of domain name
                                    #   i.e. rightmovepage.qprotocol(user values) -> rightmovepath / full rightmove url
                                    #     or just handle qprotocol separately, considering it'll just be domain dependent.
        ...
    
    def to_pretty_txt(self, dest: str) -> None:
        ...

    def is_in_json(self):
        ...


class LettingAgency:
    def __init__(self, name): 
        self.name = name  # 'chappandmatt' <- "chappellandmatthews"
        if not self.__validate_name():
            raise ValueError("Invalid agency name")

        self.domain = self.__get_domain()  # "rightmove"
        self.query_tags = self.__get_query_tags()  # [viewType, keywords, ...]
        self.url_base = ...  # "https://www.rightmove.co.uk/property-to-rent/find.html?"
        self.data = self.__load_agency_data()

    def __validate_name(self):
        return self.name in self.load_full_json()

    def __load_agency_data(self):
        if (agency_data := self.load_full_json()[self.name]) is None:
            print("Failed to load agency data")
            return None
        return agency_data

    def __get_domain(self):
        return self.__load_agency_data()["domain"]

    def __get_query_tags(self):
        return self.__load_agency_data()["query tags"]

    def load_full_json(self):
        try:
            with open("Agencies.JSON", "r") as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            # Expect two errors: one from this and one from `self.domain.__get_domain()`'s (None)['domain'] indexing
            raise JSONLoadError

    def WIP_change_name(self, new_name):
        try:
            LettingAgency(new_name).domain
        except ValueError:
            self.name = self.name



def url_in_list(input_url: str) -> bool:
    """
    Checks whether provided url has matching 'domain' and 'TLD' with those
    documented in 'final_project/agencies/agencies.txt'
    Change these variable names!
    """
    if not input_url:
        raise ValueError("No input entered")

    if search := re.search(Pattern.p4, input_url):
        input_origin = search.group(1)
    else:
        if search := re.search(Pattern.p4[:-2], input_url):
            raise ValueError("Missing '/' at end of input URL`")
        else:
            raise ValueError("Input URL does not fit expected pattern")

    # Check if origin of URLs in each row of agencies.txt matches input_origin
    with open(AGENCIESPATH + "agencies.txt", "r") as file:
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


def matches_to_txt(
    input_file: str, output_file: str, pattern: str, *catches: list
) -> None:
    """
    Searches for `pattern` matches in `input_file`, outputs matches to `output_file`
    Want to add functionality for which 'groups' of the match object to capture
    """
    try:
        attr_pattern = getattr(Pattern, pattern)
    except AttributeError:
        raise AttributeError("Invalid pattern choice")

    matches = []
    with open(input_file, "r") as file:
        for line in file:
            matches.append(re.search(attr_pattern, line))
    list_matches = []
    ## EDIT SUGGESTION ## Could probably join these loops together
    for match in matches:
        if match and match.group(1) not in list_matches:
            list_matches.append(match.group(1))
    with open(output_file, "w") as newfile:
        for match in list_matches:
            newfile.write(match + "\n")


def parse_file_to_BS(filename: str) -> BS:
    """
    Takes in a filename in 'filename.html' format
    Outputs the BS (BeautifulSoup) object, parsed in 'html'
        Read-only, encoded in utf-8
    """
    with open(filename, "r", encoding="utf-8") as file:
        return BS(file, "html.parser")


def WIP_rightmove_query_parser():
    """
    ### WIP ###
    Takes info from 'rightmove/sample_urls.txt' and makes dictionary of unique query terms

    Could strip the information before the query from the URL to save storage but cba with that yet
    Could also NOT rewrite the ENTIRE file every time it runs, but oh well -- for now.
    """
    query_tags_element = 4
    unique_tags_values = dict()

    with open(AGENCIESPATH + "rightmove/sample_urls.txt", "r") as file:

        for line_num, row in enumerate(file, start=1):
            if row.isspace() or row.lstrip()[0] == "#":
                continue

            # Isolates individual URL's query string:
            #   e.g. 'locationIdentifier=REGION%5E6574&maxBedrooms=3&maxPrice=1750..."
            url_query_tags_string = libparse.urlparse(row)[query_tags_element]

            # Converts query string to dictionary with tags as keys,
            #   and their values as... values, stored in a list.
            tag_value_dict = libparse.parse_qs(url_query_tags_string)

            ### FIX ### This has got to be able to be simplified or made quicker somehow
            for tag in tag_value_dict.keys():
                if tag in unique_tags_values.keys():  # .keys is redundant but clearer
                    for value in tag_value_dict[tag]:
                        if value not in unique_tags_values[tag]:
                            unique_tags_values[tag].append(value)
                else:
                    unique_tags_values[tag] = tag_value_dict[tag]

    with open(AGENCIESPATH + "rightmove/query_terms.txt", "w") as file:
        for index, tag in enumerate(unique_tags_values, start=1):
            file.write(f"#{index}: {tag} = {unique_tags_values[tag]}\n")


def main():
    ...


if __name__ == "__main__":
    main()
