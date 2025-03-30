""" Module for logging and plotting `Particles`. """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from src.data_types import PositionLog, Particles
from src.classes.config import Config


def log_positions(particles: Particles, position_log: PositionLog) -> None:
    """
    Takes in `Particles` and a `PositionLog`.\n
    Returns an updated `PositionLog` containing particles' positions. 
    """
    for particle in particles:
        position_log[particle.id].append(particle.position)
    return position_log


def parse_position_logs(position_logs: PositionLog) -> dict[int: tuple]:
    """
    Takes in `PositionLog` and parses its position lists to pyplot-friendly (xs,ys,zs) tuple.\n
    Example: { 0: [ [10,20,30], [11,21,31], ... ] } -> { 0: ([10,11,...], [20,21,...], [30,31,...]) }
    """
    parsed_logs = dict()
    for id, positions in position_logs.items():
        
        xs, ys, zs = list(), list(), list()
        for x, y, z in positions:
            #TODO: Got to be a better way of doing this.
            xs.append(x)
            ys.append(y)
            zs.append(z)
        parsed_logs[id] = (xs, ys, zs)
    return parsed_logs


def plot_logs(position_logs: PositionLog, config_object: Config) -> None:
    """ Takes in a `PositionLog' and `Config` object, parses it into pyplot-readable tuples, and styles and plots it in 3D. """
    parsed_logs = parse_position_logs(position_logs)

    # plt.style.use("dark_background")

    fig = plt.figure(num="Gravity Simulation")
    ax = fig.add_subplot(projection='3d')
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    pane_rgba = (.8, .8, .8, .1)
    ax.xaxis.set_pane_color(pane_rgba)
    ax.yaxis.set_pane_color(pane_rgba)
    ax.zaxis.set_pane_color(pane_rgba)
    # ax.set_axis_off()
    # ax.grid(False)

    #TODO def update(frame):

    #TODO ani = FuncAnimation(fig, update, frames=)

    for i, xyzs in parsed_logs.items():
        if config_object.scatter:
            ax.scatter(*xyzs, label=f"Particle {i}")
        elif config_object.lines:
            ax.plot(*xyzs, label=f"Particle {i}")
    # ax.legend() 

    #* Add legend
    # plt.legend(bbox_to_anchor=(1.0,1.0),\
    # bbox_transform=plt.gcf().transFigure)

    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')


    try:
        plt.show()
    except KeyboardInterrupt:
        #* Inconsistent but better than nothing.
        print("Closing Plot.")
        plt.close('all')
