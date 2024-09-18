""" Methods to generate and supply particle data for simulation purposes """

import random
import config
import logging


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


def main():
    # Generates pre-packaged tuple of all results, or user-defined results
    if config.random_inputs:
        first = MultipleResults.get_masses()
        second = MultipleResults.get_positions()
        third = MultipleResults.get_velocities()
        return (first, second, third)
    else:
        logging.info("This functionality hasn't been implemented yet")
