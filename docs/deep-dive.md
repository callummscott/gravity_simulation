# Learning Experiences

Here's a place I just wanted to write a little about some of the interesting experiences I had writing this program.

## 1. Numerical Integration Methods
When originally writing this, I intended to try to 'invent' my own way of deriving the equations of motion using what I knew about Taylor approximations. I saw online that most approximations essentially use a 2nd order approximation -- as many equations in Physics do -- and sought instead to do one better! This proved to be a pain, and I didn't know enough to be able to extrapolate as to what the third order equations of motion would be considering that it would actually demand a proper understanding of vector calculus -- an understanding that I didn't have.

I ended up facing issues with overflow and it was incredibly difficult to determine if this was a result of my likely-flawed derivations or some other error elsewhere. After scouring for a potential source for that bug literally everywhere else, I decided to relent and write more typical equations of motion using the [Velocity Verlet](https://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet) algorithm. Surely enough, those issues were resolved.

## 2. Collision Handling
In older versions with the overflow error, I thought one of the problems might be particles actually colliding and accelerations therefore overflowing, so I sought to implement some kind of a collision handling algorithm. Implementing the collision handler evidently wasn't what actually fixed the issue, but seeing just how frequently these collisions can actually happen now, I'm sure it wasn't a complete waste of time.

In the latest version though, I developed a slightly more sophisticated solution to handling collisions that I found interesting. The problem as I met it was as follows:

### Disjoint set problem
**Given some collection of unqiue pairs of integer particle IDs**, with the ID pair signifying a collision between those two particles -- for example, `[{1, 2}, {5, 4}]` represents a collision between `1` and `2`, as well as between `4` and `5` -- **group these particles into 'mutual-collision' groups** that represent chains of particles that are, at that instant, colliding with at least one member of that group.

This problem looks trivial in the aforementioned example, but consider what would happen in the --admittedly astronomically unlikely-- case of the id pairs looking like this:

```
[{15, 7}, {8, 4}, {9, 3}, {1, 2}, {2, 6}, {8, 15}, {5, 14}]
```

## 3. Leapfrogging
The Velocity Verlet algorithm relies on what's called '[leapfrogging](https://en.wikipedia.org/wiki/Leapfrog_integration)'. This is so-named because although calculating the `acceleration` of a particle in the next timestep only requires knowledge of its `position` during the prior timestep, in order to calculate the particle's next `velocity`, you must know both its prior *and* next `acceleration`; this therefore requires keeping track of the particles last state. Originally, I created new `next_position`, `next_velocity`, etc. attributes for this, but trying to stitch of all these calculations together in a cylical fashion became an absolute nightmare. I drew a graph representing the ordering of the calculations, and couldn't wrap my head around how I'm supposed to actually accomplish what looked to be a seemingly-impossible ordering with code that's executed sequentially.

![Motion Calculation Graph](/docs/motion_calculations.drawio.png)

I came to realise that I could essentially just try drag around the nodes on the graph, as above, until all of the arrows pointed from left → right and, after doing this, the solutions fell into place.

I did however later encounter a bug in which seemingly random particles were acting as though they were being collided with, at the exact moments that other particles were being collided with, and the issue turned out to be caused by the deletion of particles from a new and updated particles list without deleting the particles from the old particles list -- which again only originated from this leapfrogging.

## 4. Testing Difficulties
Given the nature of this program, it's hard to qualify when exactly it's 'doing a good simulation' besides particles just heading in the right-seeming general direction. Particle paths may look attractive and curve how you'd expect them to, but is it actually accurate? Has I implemented the equations properly? The only real way to test whether it's working as intended is by calculating the energy of the system and --collisions-aside-- ensuring that energy is approximately conserved. Even this however proved to be difficult considering the fundamentally flawed nature of numerical integration and how errors accumulate. So what constitutes a job well done?

![Euler vs Leapfrogging](https://upload.wikimedia.org/wikipedia/commons/a/ac/Euler_leapfrog_comparison.gif)

Well, the wiki page on [leapfrog integration](https://en.wikipedia.org/wiki/Leapfrog_integration) gave me an impression of how the energy is supposed to behave over time for a simulation of this kind, and all I could hope for was that its behaviour roughly resembles what we see in the gif above. By plotting the total energy of the system, and appreciating the 'impact' that collisions will have on it, I hope to see similar results.