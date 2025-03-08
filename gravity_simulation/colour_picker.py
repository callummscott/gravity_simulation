
from json import load
from random import choice
from gravity_simulation.config import Config

CONFIG = Config()

def get_colours_json():
    with open('gravity_simulation/colours.json', 'r') as json_file:
        colours_json = load(json_file)
    return colours_json


def get_colours_rgb():
    colours_json = get_colours_json()
    colours_rgb = {}
    for colour in colours_json:
        colours_rgb[colour] = colours_json[colour]
    return colours_rgb


# Trying to make this 'functional' so it doesn't use a global variable
def choose_distinct_rgb(past_choices=[]):
    """ Chooses from input past_choices and returns both the rgb value of the chosen colour, and an updated past_choices list """
    colours_json = get_colours_json()
    all_colour_names = list(colours_json)

    choice_log = []
    if past_choices:
        for colour in past_choices: 
            if (colour not in choice_log):  # Choice isn't a duplicate
                if isinstance(colour, str): # Unfortuantely can't use ternary with raise Error
                    choice_log.append(colour)
                else:
                    raise TypeError("Input is not a string")
            else:
                raise ValueError("Repeat colour choices have been made")    

        for colour in past_choices:
            if colour not in all_colour_names:
                raise IndexError("Not a recognised colour")
        if len(past_choices) == 16:
            raise IndexError("All colours have already been used up")
        
        colours_left = [ colour for colour in all_colour_names if (colour not in past_choices) ]
    else:
        colours_left = all_colour_names
    
    chosen_colour_name = choice(colours_left)
    new_past_choices = past_choices + [chosen_colour_name] # Can't just append because I want to return a new variable
    chosen_colour_rgb = colours_json[chosen_colour_name]

    return (chosen_colour_rgb, new_past_choices)


def rgb_to_0_1_format(rgb_colour):
    """ Converts distinct_rgb value to 0 -> 1 form and returns in a tuple """
    rgb_0_1_tuple = tuple(value/255.0 for value in rgb_colour)
    return rgb_0_1_tuple