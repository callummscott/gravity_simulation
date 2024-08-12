import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..')
sys.path.append( mymodule_dir )

from beautiful_soup import url_in_list
import pytest

def test_url_in_list_True():
    """
    All valid samples of URLs in the wild
    """
    assert url_in_list(r"https://www.rightmove.co.uk/properties/151239299#/?channel=RES_LET") == True
    assert url_in_list(r"https://www.rightmove.co.uk/property-to-rent/search.html?searchLocation=Bristol&useLocationIdentifier=true&locationIdentifier=REGION%5E219") == True
    assert url_in_list(r"https://www.zoopla.co.uk/to-rent/details/68058324/?search_identifier=34c6a9297d6a613e7dddf4200401563729334f8d63b83cec56543e3256f6a8d3") == True
    assert url_in_list(r"https://rentola.co.uk/property-to-rent?rent_per=month&order=rent_asc&id=dHA9NCN0dj02NmE3YzkyMyNubT1CcmlzdG9sLCBFbmdsYW5kLCBHQlIjc2M9R0IjbG5nPTQyI2xuPVdvcmxk&rent=0-1300") == True
    assert url_in_list(r"https://www.yourabode.co.uk/rent-flat-or-house-bristol/BRI070269/Brynland-Avenue-Bishopston-BS7-9DY") == True

def test_url_in_list_False():
    # Not in my registry
    assert url_in_list(r"https://www.rentll.co.uk/") == False
    # Wrong domain name
    assert url_in_list(r"https://www.brightmovie.com/") == False
    # Missing (appropriate) 'www.'
    assert url_in_list(r"https://yourabode.co.uk/rent-flat-or-house-bristol/BRI070269/Brynland-Avenue-Bishopston-BS7-9DY") == False


def test_url_in_list_ValueError():
    with pytest.raises(ValueError):
        # Not a valid URL
        url_in_list(r"BOING")
    with pytest.raises(ValueError):
        # Missing (s) from 'https'
        url_in_list(r"http://brightmovie.co.uk")
    with pytest.raises(ValueError):
        # input_url == None
         url_in_list(r"")
    with pytest.raises(ValueError):
        # Missing '.co', invalid TLD
        url_in_list(r"https://rentola.uk/property-to-rent?rent_per=month&order=rent_asc&id=dHA9NCN0dj02NmE3YzkyMyNubT1CcmlzdG9sLCBFbmdsYW5kLCBHQlIjc2M9R0IjbG5nPTQyI2xuPVdvcmxk&rent=0-1300")
