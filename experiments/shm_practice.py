import matplotlib.pyplot as plt
import numpy as np

def testing():
    print('this is just a test')

def shm() -> None:

    positions = []
    x_pos = 0 # Initial
    vel = 1 # Initial
    spring_konstant = .5
    accel = -spring_konstant*x_pos
    t, dt = 0, 1/1000
    glimpse, phase = 0, 10
    while t < 9:
        x_pos += vel*dt
        positions.append(x_pos)
        vel += accel*dt
        accel = - spring_konstant*x_pos

        if (glimpse+phase) % 100 == 0:
            print(
                f"x = {x_pos}",
                f"Velocity = {vel}", 
                f"Acceleration = {accel}",
                "------------",
                sep='\n')
        glimpse += 1

        t += dt
    print(max(positions), min(positions))

def shm2d() -> None:

    _, ax = plt.subplots()
    results_1 = initial_to_xy_coord_arrays([.7, .4], [.1, .2])
    results_2 = initial_to_xy_coord_arrays([.2, .1], [.6, 1])
    ax.plot(results_1[0], results_1[1])
    ax.plot(np.array([.7]), np.array([.4]), 'o', label='initial pos. 1')
    ax.plot(results_2[0], results_2[1])
    ax.plot(np.array([.2]),np.array([.1]), 'o', label='initial pos. 2')
    ax.legend()
    plt.show()

def initial_to_xy_coord_arrays(initial_pos_list:list, initial_vel_list:list) -> tuple:
    
    initial_pos_array = np.array(initial_pos_list)
    initial_vel_array = np.array(initial_vel_list)

    spring_konstant = 0.5
    position     = initial_pos_array
    velocity     = initial_vel_array
    acceleration = -spring_konstant*position

    dt = 1/1000
    t_max = 100
    div_number = int(t_max/dt)

    ts = np.linspace(0, t_max, div_number) # Thought arange was better but allegedly not???
    xs = np.empty(div_number)
    ys = np.empty(div_number)

    for index, _ in enumerate(ts):

        xs[index] = position[0]
        ys[index] = position[1]

        position += velocity*dt
        velocity += acceleration*dt
        acceleration = -spring_konstant*position
        
    
    return (xs, ys)

def shm3d() -> None:
    
    fig = plt.figure(figsize=plt.figaspect(0.5))

    xs, ys, zs = shm3d_initial_to_xyz_coord_arrays([1,.9,.09], [3,1,-.2])
    ax = fig.add_subplot(1,2,1, projection='3d')
    ax.plot3D(xs, ys,zs, 'blue')
    ax.plot3D(np.array([1]), np.array([.9]), np.array([.09]), 'o', label='initial pos. 1', color='blue')
    
    xs, ys, zs = shm3d_initial_to_xyz_coord_arrays_taylor([1,.9,.09], [3,1,-.2])
    ax = fig.add_subplot(1,2,2, projection='3d')
    ax.plot3D(xs, ys, zs, 'red')
    ax.plot3D(np.array([1]), np.array([.9]), np.array([.09]), 'o', label='bleh', color='red')

    plt.show()

def shm3d_initial_to_xyz_coord_arrays_taylor(initial_pos_list:list, initial_vel_list:list) -> tuple:
    initial_pos_array = np.array(initial_pos_list)
    initial_vel_array = np.array(initial_vel_list)

    spring_konstant = 0.5
    position     = initial_pos_array
    velocity     = initial_vel_array
    acceleration = -spring_konstant*position

    dt = 1/1000
    t_max = 100
    div_number = int(t_max/dt)

    ts = np.linspace(0, t_max, div_number)# Thought arange was better but allegedly not???
    xs = np.empty(div_number)
    ys = np.empty(div_number)
    zs = np.empty(div_number)

    for index, _ in enumerate(ts):

        xs[index] = position[0]
        ys[index] = position[1]
        zs[index] = position[2]

        position += dt*(velocity + dt*.5*acceleration)
        velocity += dt*(acceleration - dt*.5*spring_konstant*velocity)
        acceleration = -spring_konstant*position
        

    return (xs, ys, zs) 

def shm3d_initial_to_xyz_coord_arrays(initial_pos_list:list, initial_vel_list:list) -> tuple:
    initial_pos_array = np.array(initial_pos_list)
    initial_vel_array = np.array(initial_vel_list)

    spring_konstant = 0.5
    position     = initial_pos_array
    velocity     = initial_vel_array
    acceleration = -spring_konstant*position

    dt = 1/1000
    t_max = 100
    div_number = int(t_max/dt)

    ts = np.linspace(0, t_max, div_number)# Thought arange was better but allegedly not???
    xs = np.empty(div_number)
    ys = np.empty(div_number)
    zs = np.empty(div_number)

    for index, _ in enumerate(ts):

        xs[index] = position[0]
        ys[index] = position[1]
        zs[index] = position[2]

        position += velocity*dt
        velocity += dt*acceleration
        acceleration = -spring_konstant*position
        

    return (xs, ys, zs)

def shm_energy():
    dt, max_time = 1/100, 10

    ts, xs = [np.linspace(0, max_time, int(max_time/dt)) for i in range(2)]
    position = 10
    velocity = -.5

    for index, time in enumerate(ts):
        acceleration = ...
        
    ...

if __name__ == "__main__":
    
    ...