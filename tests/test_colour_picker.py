import pytest

from src.colour_picker import *


## GET_COLOURS_RGB ##

@pytest.mark.parametrize(
    "colour_name, colour_rgb",
    [
        ("Dk. Gray", [87,87,87]),
        ("Green", [29,105,20]),
        ("Red", [173,35,35]),
        ("Purple", [129,38,192])
    ]
)
def test_get_colours_rgb(colour_name, colour_rgb):
    colours_dictionary = get_colours_rgb()
    assert colours_dictionary[colour_name] == colour_rgb
    assert len(list(colours_dictionary)) == 16
 

@pytest.mark.parametrize("key", [-1, 3432, "blue", "Aquamarine", "Sponge", "Testring"])
def test_get_colours_rgb_key_error(key):
    with pytest.raises(KeyError):
        get_colours_rgb()[key]


@pytest.mark.parametrize("key", [[1,1,1], {"an": "unhashable"}])
def test_get_colours_rgb_type_error(key):
    with pytest.raises(TypeError):
        get_colours_rgb()[key]


## CHOOSE_DISTINCT_RGB ##

@pytest.mark.parametrize(
    "past_colours",
    [
        ([]),
        (["Tan"]),
        (["Cyan", "Pink"]),
        (['Dk. Gray', 'Purple', 'Yellow', 'Cyan', 'Pink']),
        (['Blue', 'White', 'Lt. Green', 'Pink', 'Black']),
        (['Lt. Blue', 'Dk. Gray', 'Orange', 'Purple', 'Tan']),
        (['Lt. Gray', 'Lt. Blue', 'Red', 'Black', 'Green']),
        (['Black', 'Cyan', 'Red', 'Orange', 'Dk. Gray']),
        (['Lt. Blue', 'Yellow', 'Red', 'Orange', 'Pink', 'White', 'Green'])
    ]
)
def test_choose_distinct_rgb(past_colours):
    colours_rgb = get_colours_rgb()
    chosen_colour_rgb, new_past_colours = choose_distinct_rgb(past_colours) 

    assert len(new_past_colours) == len(past_colours) + 1

    assert type(chosen_colour_rgb) == list
    assert len(chosen_colour_rgb) == 3
    for val in chosen_colour_rgb:
        assert type(val) == int
    
    for name, rgb in colours_rgb.items(): 
        if rgb == chosen_colour_rgb: # Backwards way to determine name corresponding to chosen RGB value
            assert name not in past_colours
            assert name in new_past_colours
    
    past_colours = []
    for _ in range(16):
        _, past_colours = choose_distinct_rgb(past_colours)
    assert sorted(past_colours) == sorted(list(get_colours_rgb()))


@pytest.mark.parametrize(
    "past_choices",
    [
        # -- Repeat names -- #
        ['Red', 'Cyan', 'Lt. Gray', 'Blue', 'Cyan'],
        ['Black', 'Lt. Gray', 'Lt. Gray', 'Brown', 'Purple'],
        ['Cyan', 'White', 'Green', 'White', 'Black'],
        ['Brown', 'Red', 'Cyan', 'Brown', 'Lt. Green'],
        ['Cyan', 'Brown', 'Yellow', 'Brown', 'Yellow'],
        # -- Made up names -- #
        ["Ruby", "Black", "Yellow"],
        ["Lt. Black", "Sapphire", "Tortoise"],
        ["Ocean Blue", "Burgundy", "Lime"],
    ]
)
def test_choose_distinct_rgb_value_error(past_choices):
    #* Tests for appropriate errors with duplicate input colours
    with pytest.raises(ValueError):
        test_choose_distinct_rgb(past_choices)


@pytest.mark.parametrize(
    "past_choices", [ [1, 2, 3], "test", -10,123, None]
)
def test_choose_distinct_rgb_type_error(past_choices):
    with pytest.raises(TypeError):
        choose_distinct_rgb(past_choices)


## RGB_TO_0_1_FORMAT ##

@pytest.mark.parametrize(
    "rgb_colour",
    [
        [0, 0, 0],
        [100, 100, 100],
        [123, 74, 22],
        [255, 255, 255],
        [203, 201, 198],
        [65, 21, 12]
    ]
)
def test_rgb_to_0_1_format(rgb_colour):
    rgb_0_1_format = rgb_to_0_1_format(rgb_colour)
    assert isinstance(rgb_0_1_format, tuple)
    assert len(rgb_0_1_format) == 3
    for val in rgb_0_1_format:
        assert 0 <= val <= 1


@pytest.mark.parametrize(
    "rgb_colour",
    [
        [-1,-1,-1],
        [255, 255, 256],
        [12, 34, 300],
        [0, 0, -1]
    ]
)
def test_rgb_to_0_1_format_value_error(rgb_colour):
    with pytest.raises(ValueError):
        rgb_to_0_1_format(rgb_colour)


@pytest.mark.parametrize(
    "rgb_colour",
    [
        "test",
        123,
        [123, 123, 12.3],
        ["test", "ing", "this"],
    ]
)
def test_rgb_to_0_1_format_type_error(rgb_colour):
    with pytest.raises(TypeError):
        rgb_to_0_1_format(rgb_colour)


if __name__ == "__main__":
    test_get_colours_rgb()
    test_get_colours_rgb_key_error()
    test_get_colours_rgb_type_error()

    test_choose_distinct_rgb()
    test_choose_distinct_rgb_type_error()
    test_choose_distinct_rgb_value_error()
    
    test_rgb_to_0_1_format()
    test_rgb_to_0_1_format_type_error()
    test_rgb_to_0_1_format_value_error()