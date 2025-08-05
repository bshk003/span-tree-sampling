import itertools
import matplotlib.pyplot as plt

from sampling.mcmc import MetropolisHastings
from sampling.gridspanningtree import GridSpanningTree, serpentine_path
from rendering.grid_2d import RadialRenderer


# Grid dimensions.
rows, cols = 30, 40
renderer = RadialRenderer(rows, cols)

N = 40000
RENDER_FREQ = 80

# Parameters for the energy functional of a spanning tree.
# A negative coefficient -- favor larger values, positive -- favor smaller values.
# alpha : the tree diameter
# gamma : the number of turns (passage bends)
# delta[<degree>] : node degrees contribution (<degree> in 0,1,2,3,4)
# vortex: the winding number around a chosen node (positive - CW, negative - CCW)

# Here are some example settings.

# Favor straight passages. Penalize bending and branching.
params_str = {'alpha': 30,
              'gamma': 40,
              'delta': [0, 0, -20, 30, 30],
              'vortex': {}}

#Favor long passages with many bends. Penalize branching.
params_bnd = {'alpha': 0,
              'gamma': -40,
              'delta': [0, 0, -30, 40, 40],
              'vortex': {}}

#Favor crossroads. Penalize bends and T-junctions.
params_crs = {'alpha': 0,
              'gamma': 30,
              'delta': [0, 0, 0, 30, -40],
              'vortex': {}}

# Penalize bends and junctions. Favor a vortex distortion in the bottom left area.
params_spr = {'alpha': 0,
              'gamma': 20,
              'delta': [0, 0, -30, 30, 30],
              'vortex': {(5, 5): -500}}

#initial = serpentine_path(rows, cols)
tree = GridSpanningTree(rows, cols, 
                        params=params_str, 
                        initial=None, 
                        periodic=(False, True))

# Smaller beta (higher temperature) -- more random fluctuations.
# Larger beta promotes convergence to a metastable state.
sampler = MetropolisHastings(tree, beta=0.1)

#Saving a batch of rendered frames as animation.

N_frames = N // RENDER_FREQ
renderer.save_animation(states_iterator=sampler.get_state(only_new=True),
                        num_frames=N_frames,
                        render_freq=RENDER_FREQ,
                        interval=100,
                        filename='spanning_tree_animation.gif')

# Uncomment for the on-screen visualization.

# k = 0
# for state in itertools.islice(sampler.get_state(only_new=False), N):
#     k += 1
#     if not k % RENDER_FREQ:
#         renderer.draw_configuration(state)
#         plt.pause(0.01)

plt.show()
