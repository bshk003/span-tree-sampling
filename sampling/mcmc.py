from abc import ABC, abstractmethod
import math
import random

# An abstract superclass for microstates.
class State(ABC):
    @abstractmethod
    def propose_move(self):
        # Should return (proposed_energy, move_data)
        pass

    @abstractmethod
    def make_move(self, move_data):
        pass
    
    @abstractmethod
    def energy(self):
        pass

class MetropolisHastings():
    def __init__(self, initial, beta):
        self.beta = beta # The inverse temperature.
        self.state = initial
    
    def get_state(self, only_new=False):
        while True:
            current_energy = self.state.energy()
            proposed_energy, move_data = self.state.propose_move()
            
            #pr_accept = min(1, math.exp(-self.beta * (proposed_energy - current_energy)))
            if proposed_energy <= current_energy:
                pr_accept = 1.0
            else:
                pr_accept = math.exp(-self.beta * (proposed_energy - current_energy))
            r = random.random()
            
            if r < pr_accept:
                self.state.make_move(move_data)
                yield self.state
            elif not only_new:
                yield self.state