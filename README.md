# Python Gravity Simulation
> A 3D n-body gravity simulation written in Python.

<img src="docs/gravity_simulation.png" width=640/>

## Usage
To get started, install all of the relevant packages with:
```
pip install -r requirements.txt
```
Next, just `cd` to the project's root directory and run:
```
py -m src.main        # on windows
python3 -m src.main   # on Unix/MacOS
```
To change the settings for the simulation, such as:
- the number of particles
- the number and size of the timesteps
- the maximum masses, distances, and speeds of the randomly-generated particles
- the number of points displayed in the final plot
- and more...

just check out and edit the contents of the `config.yaml` file in found in the `.config/` folder. 

## How it works
1. Config values are read from `config.yaml` that dictate how random particles are generated.
2. These values are used to generate `Particle` objects that store information about each particle's state
3. Gravity calculations are performed on a list of particles per timestep, while checks for collisions take place
4. If collisions are found, collision groups are identified and 'merged' with the largest particle, with their momenta being conserved.
5. Particle positions are read at a config-value derived rate and stored in position logs.
6. These particle positions are finally parsed and plotted in 3D using pyplot!

## Potential Improvements
- **Animation**: I've already tried to get animations working but despite some success on a smaller scale, it's proving difficult to achieve with a dynamically set number of particles. Visuals of particles floating around and leaving behind a trail is surely a tremendous improvement over what currently is, but this is so the best I'm able to achieve.
- **Utilising more NumPy**: Only after building confidence with libraries throughout this project have I realised just how much could be rewritten with greater use of `numpy`. This version is itself essentially a complete overhaul that I managed to squeeze into less than a week, and yet I feel immediately that another one is already due. I was also proud of my creation of the `permutations` module that I made use of throughout, only to also eventually find that `itertools` already offers things like `combinations` and `product` that I could have been using.
- **Mass-based particle sizing**: Seeing how straightforward it is to dynamically size the scatter points in pyplot (i.e. by just defining `s=`), it immediately became apparent that if I kept some kind of parallel log of the mass (or changes to it) then not only could I straightforwardly illustrate the masses of particles, but I could even dynamically change it when collisions with other particles occurred.
- **Particle arrangement presets**: I orignally set out to make this thinking that I'd be able to hardcode the actual positions of the Sun, Earth and Moon to predict where they'll all be over time. The reality of that goal eventually set in and I figured that a general N-body simulation would be a good compromise. Having made it now though, I think it's probably not too hard to just add in a 'pre-configured particles' option that loads a preset that at the very least loosely resembles the motion of our solar system.
- **Darkmode**: I wanted to make the plots dark by default, but the default way of achieving this leaves the particle colours looking weirdly faded, but although this is something that's probably much easier to implement than the other improvements, I'm shelving it for now.

## What now?
Thanks for reading! If you want to read a little bit more about the thought behind the code, check out `docs/deep-dive.md`.

Enjoy messing around with it! - `Callum`


