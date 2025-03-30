""" Module for logging and plotting `Particles`. """

import matplotlib.pyplot as plt
from src.data_types import PositionLog, Particles


def log_positions(particles: Particles, position_log: PositionLog) -> None:
    """
    Takes in `Particles` and a `PositionLog`.\n
    Returns an updated `PositionLog` containing particles' positions. 
    """
    for particle in particles:
        position_log[particle.id].append(particle.position)
    return position_log


def parse_position_logs(position_logs: PositionLog):
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


def plot_logs(position_logs: PositionLog) -> None:
    """ Takes in a `PositionLog', parses it into pyplot-readable tuples and plots in 3D. """
    parsed_logs = parse_position_logs(position_logs)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for _, xyzs in parsed_logs.items():
        ax.scatter(*xyzs)

    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')

    try:
        plt.show()
    except KeyboardInterrupt:
        print("Closing Plot.")
