import random

class CubeMatrix:
    def __init__(self, length, width):
        self.world = [[None for _ in range(width)] for _ in range(length)]
        self.grasped_block = None
        self.logging = []
        self.populate_world_randomly()

    def populate_world_randomly(self):
        block_types = ['A', 'B', 'C', 'D']
        num_blocks = random.randint(1, len(self.world) * len(self.world[0]) // 2)
        for _ in range(num_blocks):
            x, y = random.randint(0, len(self.world) - 1), random.randint(0, len(self.world[0]) - 1)
            if self.world[x][y] is None:
                self.world[x][y] = random.choice(block_types)
        self.display_world()

    def display_world(self):
        for row in self.world:
            print(' '.join(['_' if cell is None else cell for cell in row]))
        print()

    def grasp(self, x, y):
        if 0 <= x < len(self.world) and 0 <= y < len(self.world[0]) and self.world[x][y] is not None:
            self.grasped_block = (x, y, self.world[x][y])
            self.logging.append(f"Grasped {self.grasped_block[2]} from ({x}, {y})")
            self.world[x][y] = None  # Remove the block from the world as it's being grasped
            print(f"Grasped {self.grasped_block[2]} from ({x}, {y})")
            self.display_world()
        else:
            self.logging.append("Attempted to grasp but no block was found.")
            print("No block to grasp at the specified coordinates.")

    def step_move(self, from_x, from_y, to_x, to_y):
        # Direction of movement for x and y
        dir_x = 1 if to_x > from_x else -1 if to_x < from_x else 0
        dir_y = 1 if to_y > from_y else -1 if to_y < from_y else 0
        
        block_id = self.grasped_block[2]
        self.world[from_x][from_y] = None  # Clear the block from the original position

        while (from_x != to_x or from_y != to_y):
            # Move block by one step
            if from_x != to_x:
                from_x += dir_x
            elif from_y != to_y:
                from_y += dir_y

            # Update world with new block position for this step
            self.world[from_x][from_y] = block_id
            self.display_world()  # Display the world state at this step
            self.world[from_x][from_y] = None  # Clear the block for the next step
            self.logging.append(f"Block {block_id} moved to ({from_x}, {from_y})")
        
        # The final position after the loop is the destination
        self.grasped_block = (to_x, to_y, block_id)

    def move(self, to_x, to_y):
        if not self.grasped_block:
            self.logging.append("Attempted to move but no block was grasped.")
            print("No block grasped.")
            return

        # Execute the step by step move
        self.step_move(*self.grasped_block[:2], to_x, to_y)

        # After moving the block step by step, place it at the destination
        block_id = self.grasped_block[2]
        self.world[to_x][to_y] = block_id  # Set the block to its new position
        
        # Check for and remove adjacent matching blocks
        removed = self.remove_adjacent_matching_blocks(to_x, to_y, block_id)
        if removed:
            self.world[to_x][to_y] = None  # Remove the moved block if necessary

        self.logging.append(f"Moved {block_id} to ({to_x}, {to_y})")

        self.grasped_block = None  # Clear the grasped block
        
        self.display_world()  # Display the final world state

    def remove_adjacent_matching_blocks(self, x, y, block_id):
        # This method checks for adjacent blocks and removes them if they match the block_id.
        # Returns True if the block itself should be removed, False otherwise.
        adjacent_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        should_remove_self = False
        for adj_x, adj_y in adjacent_positions:
            if 0 <= adj_x < len(self.world) and 0 <= adj_y < len(self.world[0]):
                if self.world[adj_x][adj_y] == block_id:
                    self.world[adj_x][adj_y] = None  # Remove adjacent block
                    should_remove_self = True
                    self.logging.append(f"Adjacent block {block_id} at ({adj_x}, {adj_y}) removed")

        if should_remove_self:
            self.world[x][y] = None  # Remove the block itself
        return should_remove_self


    def cmd_handler(self):
        print("Type 'quit' to exit.")
        while True:
            cmd = input("Enter command: ").strip().lower()
            if cmd == 'quit':
                print("Quitting program.")
                break
            elif cmd.startswith("grasp") and len(cmd.split()) == 3:
                _, x, y = cmd.split()
                self.grasp(int(x), int(y))
            elif cmd.startswith("move") and len(cmd.split()) == 3:
                _, to_x, to_y = cmd.split()
                self.move(int(to_x), int(to_y))
            else:
                print("Unknown command. Use 'grasp x y' or 'move x y'.")

    def save_logs_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for log_entry in self.logging:
                file.write(log_entry + '\n')

def main():
    length, width = map(int, input("Enter the length and width of the world: ").split())
    world = CubeMatrix(length, width)
    world.cmd_handler()
    world.save_logs_to_file('cube_logs.txt')

main()
