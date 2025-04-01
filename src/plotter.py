""" Module for logging and plotting `Particles`. """

import matplotlib.pyplot as plt

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


def plotter(ax, xyzs: tuple, plot_type: str, **param_dict: dict): # Only God knows what the type is.
    """ Takes in an `axes` argument, xyz positions and  """
    if plot_type == "scatter":
        out = ax.scatter(*xyzs, **param_dict)
    elif plot_type == "lines":
        out = ax.plot(*xyzs, **param_dict)
    return out


def plot_logs(position_logs: PositionLog, config_object: Config) -> None:
    """ Takes in a `PositionLog' and `Config` object, parses it into pyplot-readable tuples, and styles and plots it in 3D. """
    parsed_logs = parse_position_logs(position_logs)

    fig = plt.figure(label="Gravity Simulation")
    ax = fig.add_subplot((0,.01,1,1), projection='3d')

    pane_rgba = (.8,.8,.8,.1)
    ax.xaxis.set_pane_color(pane_rgba)
    ax.yaxis.set_pane_color(pane_rgba)
    ax.zaxis.set_pane_color(pane_rgba)

    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')

    if config_object.scatter:
        for id, xyzs in parsed_logs.items():
            plotter(ax, xyzs, "scatter", s=config_object.marker_size, label=f"Particle {id}")
    if config_object.lines:
        for i, xyzs in parsed_logs.items():
            plotter(ax, xyzs, "lines", label=f"Particle {id}")


    try:
        plt.show()
    except KeyboardInterrupt:
        #* Inconsistent but occasionally better than nothing.
        print("Closing Plot.")
        plt.close('all')
