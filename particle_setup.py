""" Methods to generate and supply particle data for simulation purposes """

import random
import config
import json
import logging
logger = logging.getLogger(__name__)


random.seed(config.random_seed)


class SingleResult:
    # Functions that generate single random results
    def get_mass():
        return random.random()*config.max_mass

    def get_position():
        return [random.uniform(-1,1)*config.max_distance for _ in range(3)]

    def get_velocity():
        return [random.uniform(-1,1)*config.max_speed for _ in range(3)]

class MultipleResults:
    # Functions that generate one random result for every `config.number_of_particle`
    def get_masses():
        return [SingleResult.get_mass() for _ in range(config.number_of_particles)]

    def get_velocities():
        return [SingleResult.get_velocity() for _ in range(config.number_of_particles)]

    def get_positions():
        return [SingleResult.get_position() for _ in range(config.number_of_particles)]

class Visuals:

    @classmethod
    def check_particle_number():
        """ Just does a simple check that the particle number doesn't exceed the number of colours """
        if config.number_of_particles > 16:
            logging.critical("Too many particles; not enough colours!")

    @classmethod
    def get_colours_data(cls):
        """ Retrives colours from colours.json in Python dict form """
        with open('colours.json', 'r') as json_file:
            return json.load(json_file)

    @classmethod
    def get_colours_rgb(cls):
        """ Returns dictionary of colour names to [R,G,B] values """
        colours_json = cls.get_colours_data()
        colours_rgb = {}

        for colour in colours_json:
            colours_rgb[colour] = colours_json[colour]['RGB']
        
        return colours_rgb

    @classmethod
    def choose_distinct_rgb(cls):
        """ Selects a colour at random and removes it from pool to be next chosen from """

        if len(cls.colours_chosen) >= 16:
            raise IndexError("All colours have already been used up!")
        
        colours_left = [colour for colour in cls.get_colours_rgb() if colour not in Visuals.colours_chosen]
        choice = random.choice(colours_left)
        cls.colours_chosen.add(choice)

        return cls.get_colours_rgb()[choice]
    
    @classmethod
    def get_distinct_rgb_tuple(cls):
        """ Converts distinct_rgb value to 0 -> 1 form and returns in a tuple """
        rgb_0_255_list = cls.choose_distinct_rgb()
        rgb_0_1_tuple = (value/255.0 for value in rgb_0_255_list)
        return tuple(rgb_0_1_tuple)
    
    colours_chosen = set()


def get_input_variables():
    config.for_logging
    # Generates pre-packaged tuple of all results, or user-defined results
    if config.random_inputs:
        first = MultipleResults.get_masses()
        second = MultipleResults.get_positions()
        third = MultipleResults.get_velocities()
        logger.info('Sending input variables') 
        return (first, second, third)
    else:
        logger.info("This functionality hasn't been implemented yet")
