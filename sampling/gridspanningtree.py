import networkx as nx
import math, random
from sampling.mcmc import State

class GridSpanningTree(State):
    def __init__(self, rows, cols, *, params, initial=None, periodic=False):
        self.rows = rows
        self.cols = cols
        self.params = params

        self.background = nx.grid_2d_graph(rows, cols, periodic=periodic)

        if initial:
            self.tree = initial
        else:
            #self.tree = nx.random_spanning_tree(self.background)
            self.tree = GridSpanningTree.aldous_broder(self.background)

        self.complement = nx.Graph()        
        self.complement.add_nodes_from(self.background.nodes())
        
        for u, v in self.background.edges():
            if not self.tree.has_edge(u, v):
                self.complement.add_edge(u, v)

    def propose_move(self):
        complement_edges = list(self.complement.edges())
        if not complement_edges:
            return self.energy(), (None, None) # No moves possible.
            
        new_edge = random.choice(complement_edges)
        
        tmp_tree = self.tree.copy()
        tmp_tree.add_edge(*new_edge)

        # A cycle will necessarily emerge upon adding a new edge.
        cycle = nx.find_cycle(tmp_tree, source=new_edge[0])    
        to_remove_edge = random.choice(cycle)

        tmp_tree.remove_edge(*to_remove_edge)
        
        return self.calculate_energy(tmp_tree, self.params), (new_edge, to_remove_edge)
    
    def make_move(self, add_remove_edges):
        new_edge, to_remove_edge = add_remove_edges
        
        if new_edge is None:
            return
            
        self.tree.add_edge(*new_edge)
        self.tree.remove_edge(*to_remove_edge)
        self.complement.add_edge(*to_remove_edge)
        self.complement.remove_edge(*new_edge)

    def aldous_broder(graph):
        # The Aldous-Broder algorithm. Returns a random spanning tree of a graph (uniformly chosen). 
        # This can be used to create an initial state.  
        tree = nx.Graph()
        nodes = list(graph.nodes())
        start_node = random.choice(nodes)
        visited = {start_node}
        tree.add_node(start_node)
        
        cur = start_node
        while len(visited) < len(nodes):
            nxt = random.choice(list(graph.neighbors(cur)))            
            if nxt not in visited:
                tree.add_edge(cur, nxt)
                visited.add(nxt)
            cur = nxt

        return tree
    
    def energy(self, configuration=None):
        if configuration == None:
            configuration = self.tree
        
        return self.calculate_energy(configuration, self.params)
    
    @staticmethod
    def calculate_energy(tree, params):        
        # Contributions to the energy functional.
        # A negative coefficient -- favor larger values, positive -- penalize.
        # alpha : the tree diameter
        # gamma : the number of turns
        # delta : control node degrees distribution
        # vortex: the winding number around a chosen node (positive - CCW, nagative - CW)
     
        return params['alpha'] * GridSpanningTree.tree_diameter(tree) + \
               params['gamma'] * GridSpanningTree.count_turns(tree) + \
               sum(params['delta'][tree.degree[node]] for node in tree.nodes()) + \
               sum(coeff * GridSpanningTree.count_winding(tree, vortex) for vortex, coeff in params['vortex'].items())
    
    @staticmethod
    def tree_diameter(tree):
        node = random.choice(list(tree.nodes))

        dist_to = nx.shortest_path_length(tree, source=node) # Returns a dict.
        leaf = max(dist_to, key=dist_to.get)
        
        # The diameter is the largest leaf-to-leaf distance.
        return max(nx.shortest_path_length(tree, source=leaf).values())
    
    @staticmethod
    def count_turns(tree):
        res = 0
        
        for node in tree.nodes():
            if tree.degree(node) == 2:
                n1, n2 = tree.neighbors(node)                
                res += n1[0] != n2[0] and n1[1] != n2[1]
        return res

    @staticmethod
    def count_winding(tree, v):   
        RADIUS = 10
        res = 0

        path_lengths_from_v = nx.single_source_shortest_path_length(tree, source=v, cutoff=RADIUS)
        
        for u in path_lengths_from_v:
            for w in tree.neighbors(u):
                if w in path_lengths_from_v and path_lengths_from_v[w] > path_lengths_from_v[u]:
                    vector_u = (u[0] - v[0], u[1] - v[1])
                    vector_w = (w[0] - v[0], w[1] - v[1])

                    # cross_product = vector_u[0] * vector_w[1] - vector_u[1] * vector_w[0]
                    # delta_angle = cross_product and (1 if cross_product > 0 else -1)
            
                    angle_u = math.atan2(vector_u[1], vector_u[0])
                    angle_w = math.atan2(vector_w[1], vector_w[0])            
                    delta_angle = angle_w - angle_u
                    
                    if delta_angle > math.pi:
                        delta_angle -= 2 * math.pi
                    elif delta_angle < -math.pi:
                        delta_angle += 2 * math.pi
            
                    res += delta_angle

                    
        return res         
    

def serpentine_path(rows, cols):
    path_tree = nx.Graph()
    path_tree.add_nodes_from(nx.grid_2d_graph(rows, cols).nodes())
    
    for i in range(rows):
        for j in range(cols - 1):
            path_tree.add_edge((i, j), (i, j + 1))
    for i in range(rows-1):
        if i & 1:
            path_tree.add_edge((i, 0),  (i + 1, 0))
        else:
            path_tree.add_edge((i, cols-1), (i+1, cols-1))

    return path_tree