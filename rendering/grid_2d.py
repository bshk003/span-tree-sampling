import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import math

class GridRenderer():

    EDGE_COLOR = 'blue'
    EDGE_WIDTH = 1.8
    NODE_COLOR = 'skyblue'
    NODE_SIZE = 0

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.pos = {(i, j): (i, j) for i in range(rows) for j in range(cols)}

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.tight_layout()
        self.ax.set_axis_off()


    def draw_configuration(self, state):       
        self.ax.clear()        
        # Draw the tree on the single axes object.
        nx.draw(state.tree, pos=self.pos, ax=self.ax, 
                node_size=GridRenderer.NODE_SIZE,
                node_color=GridRenderer.NODE_COLOR,
                edge_color=GridRenderer.EDGE_COLOR,
                width=GridRenderer.EDGE_WIDTH,
                with_labels=False)
        
    def save_animation(self, states_iterator, num_frames, render_freq, interval, filename='animation.gif'):

        def update(frame):
            for _ in range(render_freq):
                state = next(states_iterator)
            self.draw_configuration(state)
            #self.ax.set_title(f'Step: {frame * render_freq}')
            print (f'Frame {frame+1}/{num_frames} processed.')
            return self.ax.get_children()

        try:
            ani = FuncAnimation(self.fig, update, 
                                frames=range(num_frames), 
                                interval=interval, 
                                blit=False)
            ani.save(filename, writer='pillow')
            print(f'Animation saved as {filename}')

        except Exception as e:
            print (f'Error while rendering and saving animation: {e}')
            
    
class RadialRenderer():

    EDGE_COLOR = 'blue'
    EDGE_WIDTH = 1.8
    NODE_COLOR = 'skyblue'
    NODE_SIZE = 0
    RADIUS_INNER = 10
    RADIUS_OUTER = 60

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        if rows > 1:
            delta_r = (RadialRenderer.RADIUS_OUTER - RadialRenderer.RADIUS_INNER) / (rows - 1)
        else:
            delta_r = 0
        
        if cols > 1:
            delta_theta = 2 * math.pi / (cols - 1)
        else:
            delta_theta = 0

        circle_points = [(math.cos(delta_theta * j), math.sin(delta_theta * j)) for j in range(cols)]

        self.pos = {}
        r = RadialRenderer.RADIUS_INNER 
        for i in range(rows):
            for j in range(cols):
                self.pos[(i, j)] = (r * circle_points[j][0], r * circle_points[j][1])
            r += delta_r

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.tight_layout()
        self.ax.set_axis_off()


    def draw_configuration(self, state):       
        self.ax.clear()        
        # Draw the tree on the single axes object.
        nx.draw(state.tree, pos=self.pos, ax=self.ax, 
                node_size=GridRenderer.NODE_SIZE,
                node_color=GridRenderer.NODE_COLOR,
                edge_color=GridRenderer.EDGE_COLOR,
                width=GridRenderer.EDGE_WIDTH,
                with_labels=False)
        
    def save_animation(self, states_iterator, num_frames, render_freq, interval, filename='animation.gif'):

        def update(frame):
            for _ in range(render_freq):
                state = next(states_iterator)
            self.draw_configuration(state)
            #self.ax.set_title(f'Step: {frame * render_freq}')
            print (f'Frame {frame+1}/{num_frames} processed.')
            return self.ax.get_children()

        try:
            ani = FuncAnimation(self.fig, update, 
                                frames=range(num_frames), 
                                interval=interval, 
                                blit=False)
            ani.save(filename, writer='pillow')
            print(f'Animation saved as {filename}')

        except Exception as e:
            print (f'Error while processing and saving animation: {e}')