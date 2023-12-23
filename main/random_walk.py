import mesa


class RandomWalker(mesa.Agent):
    grid = None
    x = None
    y = None
    # use a Moore neighborhood
    moore = False

    def __init__(self, unique_id, pos, model, moore=False):
       
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
      
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
