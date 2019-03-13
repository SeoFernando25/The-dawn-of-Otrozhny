

import entities
class Level():
    currentMap = None

    def __init__(self, grid, grid_entities, node_entities=None):
        self.grid = grid
        self.grid_entities = grid_entities
        self.node_entities = node_entities
        self.level_width = len(grid[0]) 
        self.level_height = len(grid) 

        # Sorry I did not had time to organize it in a better way :/
        self.num_of_collectibles = sum(isinstance(x, entities.Collectible) for x in self.grid_entities)
        self.num_of_collected = 0
        entities.Player.instance = next((x for x in self.grid_entities if type(x) == entities.Player), None)

    @staticmethod
    def load(level_object):
        
        Level.currentMap = Level(level_object.grid, level_object.grid_entities)
    
  

    def pick_random_point(self):
        import random
        random_w = random.randint(0, self.level_width - 1) 
        random_h = random.randint(0, self.level_height - 1)
        random_position =  (random_w, random_h) 
        if self.grid[random_w] [random_h] != 0:
            while self.grid[random_w] [random_h] != 0:
                random_w = random.randint(0, self.level_width - 1)
                random_h = random.randint(0, self.level_height - 1)
                random_position =  (random_w, random_h) 
        return random_position
    
