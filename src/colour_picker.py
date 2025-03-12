
from json import load
from random import choice
from src.classes.config import Config

CONFIG = Config()


def get_colours_rgb():
    """ Returns a dictionary of colour name strings to list of [R,G,B] values """
    with open('src/colours.json', 'r') as json_file:
        colours_json = load(json_file)
    return colours_json


# Trying to make this 'functional' so it doesn't use a global variable
def choose_distinct_rgb(past_choices=[]):
    """ Chooses from input `past_choices` and returns both the [R,G,B] value of a randomly chosen colour, and an updated `past_choices` list """
    if not isinstance(past_choices, list):
        raise TypeError("Past choices must be a list")
    colours_rgb = get_colours_rgb()
    all_colour_names = list(colours_rgb)

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
                raise ValueError("Not a recognised colour")
        if len(past_choices) == 16:
            raise KeyError("All colours have already been used up")
        
        colours_left = [ colour for colour in all_colour_names if (colour not in past_choices) ]
    else:
        colours_left = all_colour_names
    
    chosen_colour_name = choice(colours_left)
    new_past_choices = past_choices + [chosen_colour_name] # Can't just append because I want to return a new variable
    chosen_colour_rgb = colours_rgb[chosen_colour_name]

    return (chosen_colour_rgb, new_past_choices)


def rgb_to_0_1_format(rgb_colour):
    """ Converts distinct_rgb value to 0 -> 1 form and returns in a tuple """
    if not isinstance(rgb_colour, list):
        raise TypeError("RGB must be provided in list format")
    if not len(rgb_colour) == 3:
        raise TypeError("RGB must consist of 3 values")
    for val in rgb_colour:
        if not isinstance(val, int):
            raise TypeError("Individual RGB values must be integers")
        if (val < 0 or val > 255):
            raise ValueError("Values must lie within 0-255")
    rgb_0_1_tuple = tuple(value/255.0 for value in rgb_colour)
    return rgb_0_1_tuple