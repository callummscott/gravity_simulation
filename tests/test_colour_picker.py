
from pytest import raises
from random import shuffle

from src.colour_picker import get_colours_rgb, choose_distinct_rgb, get_colours_json

# Omitting get_colours_json since it's kinda stupid

def test_get_colours_rgb():

    #* Tests that the return value functions as expected as a dictionary
    colours_dictionary = get_colours_rgb()

    assert colours_dictionary['Dk. Gray'] == [87, 87, 87]
    assert colours_dictionary['Green'] == [29, 105, 20]
    assert colours_dictionary['Red'] == [173, 35, 35]
    assert colours_dictionary['Purple'] == [129, 38, 192]

    assert len(list(colours_dictionary)) == 16
 
    with raises(KeyError):
        colours_dictionary[0]
        colours_dictionary['blue']
        colours_dictionary[-1]
        colours_dictionary[[1,1,1]]


def test_choose_distinct_rgb():

    example_past_choices = [
        ["Tan"],
        ["Cyan", "Pink"],
        ['Dk. Gray', 'Purple', 'Yellow', 'Cyan', 'Pink'],
        ['Blue', 'White', 'Lt. Green', 'Pink', 'Black'],
        ['Lt. Blue', 'Dk. Gray', 'Orange', 'Purple', 'Tan'],
        ['Lt. Gray', 'Lt. Blue', 'Red', 'Black', 'Green'],
        ['Black', 'Cyan', 'Red', 'Orange', 'Dk. Gray'],
        ['Lt. Blue', 'Yellow', 'Red', 'Orange', 'Pink', 'White', 'Green']
    ]

    #* Tests: 1) chosen colour not in past choices, 2) chosen colour is in the updated list of past choices, 3) length of new list of past choices is only 1 greater than old list
    colours_json = get_colours_json()
    for test_case in example_past_choices:
        for _ in range(16): # (Hopefully) Chooses different new colours each iteration
            chosen_colour_rgb, new_past_choices = choose_distinct_rgb(past_choices=test_case) 
            assert len([colour for colour in new_past_choices if type(colour) == str]) == len(new_past_choices)

            new_colours = [ colour for colour in new_past_choices if (colour not in test_case)]
            assert len(new_colours) == 1
            assert colours_json[new_colours[0]] == chosen_colour_rgb

            assert chosen_colour_rgb in colours_json.values()
            assert len(test_case) == len(new_past_choices) - 1
    
    assert type(choose_distinct_rgb()) == tuple
    rgb, name = choose_distinct_rgb()
    assert (type(rgb) == list) and (len(rgb) == 3) and len([i for i in rgb if type(i) == int]) == 3
    assert (type(name) == list) and (len(name) == 1) and (len([i for i in name if type(i) == str]) == 1)
    
    #* Tests for appropriate errors with duplicate input colours
    with raises(ValueError):
        choose_distinct_rgb(past_choices=['Red', 'Cyan', 'Lt. Gray', 'Blue', 'Cyan'])
        choose_distinct_rgb(past_choices=['Black', 'Lt. Gray', 'Lt. Gray', 'Brown', 'Purple'])
        choose_distinct_rgb(past_choices=['Cyan', 'White', 'Green', 'White', 'Black'])
        choose_distinct_rgb(past_choices=['Brown', 'Red', 'Cyan', 'Brown', 'Lt. Green'])
        choose_distinct_rgb(past_choices=['Cyan', 'Brown', 'Yellow', 'Brown', 'Yellow'])

    with raises(IndexError):
        #* Tests that entering in all possible colours raises IndexError: none left to choose
        all_possible_choices = list(get_colours_rgb())
        for _ in range(10):
            shuffle(all_possible_choices)
            choose_distinct_rgb(past_choices=all_possible_choices)
        
        #* Tests that non-existant colours raise errors
        choose_distinct_rgb(["Ruby", "Black", "Yellow"])
        choose_distinct_rgb(["Lt. Black", "Sapphire", "Tortoise"])
        choose_distinct_rgb(["Ocean Blue", "Burgundy", "Lime"])

    #? Do I even bother checking for incorrect types?


def test_get_distinct_rgb_tuple():
    ...
    #TODO: Can't really do this until I've sorted out its functionality in the actual program.


if __name__ == "__main__":
    test_get_colours_rgb()
    test_choose_distinct_rgb()
    # test_get_distinct_rgb_tuple()