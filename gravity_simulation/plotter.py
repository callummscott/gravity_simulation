import matplotlib.pyplot as plt
from time import time

from gravity_simulation.config import Config
from gravity_simulation.position_log import PositionLog

from gravity_simulation.colour_picker import choose_distinct_rgb
from gravity_simulation.colour_picker import rgb_to_0_1_format


CONFIG = Config()


def get_filtered_xyz_values(position_log: dict) -> dict:
    """ Returns a dictionary of { Particle key: position log }, where some data is being filtered out for plot framerate """
    #* Builds a blank output data structure
    print("Filtering data-points before plotting")
    filtered_positions = dict()
    #* Iterates across each particle and its position log
    #*  > Length of of position logs across particles can vary
    for id, log in position_log.items(): # essentially, log = [ [x,y,z], [x,y,z], ... ]
        xs, ys, zs = log.xs, log.ys, log.zs
        filtered_xs, filtered_ys, filtered_zs  = [], [], []
        for i in range(len(xs)):
            if i % CONFIG.simple_log_rate == 0:
                CONFIG.logger.info(f"{i}: {xs[i]}, {ys[i]}, {zs[i]}")
                filtered_xs.append(xs[i])
                filtered_ys.append(ys[i])
                filtered_zs.append(zs[i])
        filtered_positions[id] = (filtered_xs, filtered_ys, filtered_zs)
    print(f"Number of points: {3*len(filtered_xs)}")
    return filtered_positions


def plot_results_3d(filtered_positions: dict[int:PositionLog]):
    """ Takes in a dictionary of { particle key : filtered position log }, generates 3D plot """

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    past_colours = []
    for id, log in filtered_positions.items():
        xs, ys, zs = log
        particle_colour_rgb, new_past_colours = choose_distinct_rgb(past_colours)
        particle_colour_0_1 = rgb_to_0_1_format(particle_colour_rgb)
        past_colours = new_past_colours #? Change the function to one that just appends the chosen colour? 
        ax.scatter3D(xs, ys, zs, marker='o', color=particle_colour_0_1, label=f"{id}")
        ax.plot3D(xs, ys, zs)
        ax.text3D(xs[0], ys[0], zs[0], f"Particle {id}")
        ax.legend()

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    ax.axis('equal')

    yield time()

    plt.show()
