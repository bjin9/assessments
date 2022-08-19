import json
import logging


class ZombieApocalypse:
    def __init__(self):
        self.grid_size = 0
        self.moving_zombies = []
        self.finished_zombies = []
        self.creatures = []
        self.creatures_dict = {}
        self.zombie_moves = ""
        self.active_zombie_index = 0


    def read_json(self, path):
        try:
            with open(path) as f:
                data = json.load(f)
            self.grid_size = data['grid_size']
            self.moving_zombies = [(data['initial_zombie'][0], data['initial_zombie'][1])]
            self.creatures = [(creature[0], creature[1]) for creature in data['creatures']]
            self.zombie_moves = data["zombie_moves"]
            self.creatures_dict = {str(creature): creature for creature in self.creatures}
            self.creatures = []
        except Exception as e:
            logging.error(f"read_json() exception: {e}")


    def print_2d_list(self, positions):
        if not positions:
            print("none")
        else:
            for pos in positions:
                print(f"({pos[0]},{pos[1]}) ", end="")
            print()


    def print_results(self):
        print("zombies' positions:")
        self.print_2d_list(self.finished_zombies)
        print("creatures' positions:")
        self.print_2d_list(self.creatures)


    def move_zombie(self, move, zombie):
        if move == 'R':
            zombie = ((zombie[0] + 1) % self.grid_size, zombie[1])
        elif move == 'L':
            zombie = ((zombie[0] + self.grid_size - 1) % self.grid_size, zombie[1])
        elif move == 'D':
            zombie = (zombie[0], (zombie[1] + 1) % self.grid_size)
        elif move == 'U':
            zombie = (zombie[0], (zombie[1] + self.grid_size - 1) % self.grid_size)
        logging.info(f"zombie {self.active_zombie_index} moved to ({zombie[0]},{zombie[1]})")
        return zombie


    def infect_creature(self, zombie):
        new_zombie = self.creatures_dict.pop(str(zombie), None)
        if new_zombie:
            logging.info(f"zombie {self.active_zombie_index} infected creature at ({zombie[0]},{zombie[1]})")
        return new_zombie


    def simulate(self):
        self.active_zombie_index = 0
        while self.moving_zombies:
            zombie = self.moving_zombies.pop(0)
            for move in self.zombie_moves:
                zombie = self.move_zombie(move, zombie)
                new_zombie = self.infect_creature(zombie)
                if new_zombie:
                    self.moving_zombies.append(new_zombie)
            self.finished_zombies.append(zombie)
            self.active_zombie_index += 1
        self.creatures = [creature for key, creature in self.creatures_dict.items()]


    def run(self):
        logging.info("creating a new zombie world!")
        self.read_json("input.json")
        self.simulate()
        self.print_results()


if __name__ == "__main__":
    logging.basicConfig(filename='zombie.log', level=logging.INFO)
    simulator = ZombieApocalypse()
    simulator.run()
