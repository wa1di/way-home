import random

class Drunk:
    '''
    This represents a drunk person who includes an own time measure, a distance
    measure, and may be made to behave differently depending on the task.
    '''
    def __init__(self, task):
        self.time = 0  # Start time
        self.velocity = 2 # Walk speed
        self.task = task
        if task == "A":
            self.position = (0, 0)
        elif self.task == "B" or self.task == "C":
            self.position = (0., 0.) # Float point values for tasks B and C
        else: 
            ValueError("Invalid Task")

    def move(self):
        if self.task == "A":
            rand_value = random.random()
            if rand_value < 0.25:
                self.position = (self.position[0] - self.velocity, self.position[1]) # Move left
            elif rand_value < 0.5:
                self.position = (self.position[0] + self.velocity, self.position[1]) # Move right
            else:
                self.position = (self.position[0], self.position[1] + self.velocity) # Move straight
        elif self.task == "B":
            pass # Implement task B here
        elif self.task == "C":
            pass # Implement task C here
        self.time += 1  # Increment time
    
    def get_vertical_position(self):
        '''
        Convenient function useful to determine whether the drunk is at the 
        danger area or not
        '''
        return self.position[1]

class Zone:
    '''
    Just a helper structure class that's used in the class Street.
    '''
    def __init__(self, zone_type, length):
        self.zone_type = zone_type  # 'safe' or 'dangerous'
        self.length = length  # Length of the zone in meters

class Street:
    '''
    Models the street, defining the safe and dangerous areas, as well as the
    likelihood to be hit by a car at each of the time steps
    '''
    def __init__(self):
        self.zones = [
            Zone('safe', 1),
            Zone('dangerous', 2),
            Zone('safe', 2),
            Zone('dangerous', 2),
            Zone('safe', 1)
        ]
        self.probability_of_hit_on_danger_zone = 0.05

    def get_street_size(self):
        '''
        Total street size 
        '''
        return sum([zone.length for zone in self.zones])

    def get_zone_at_position(self, position):
        '''
        Are we at a safe zone of the street or not?
        '''
        current_position = 0
        for zone in self.zones:
            if current_position <= position < current_position + zone.length:
                return zone.zone_type
            current_position += zone.length
        return None  # Position is out of bounds

  
class Grid:
    '''
    Includes interactions betewen the drunk and the street
    '''
    def __init__(self, drunk, street):
        self.drunk = drunk
        self.street = street
    
    def check_collision(self):
        '''
        Was there a collision between the drunk and a car on the street?
        '''
        if self.street.get_zone_at_position(self.drunk.get_vertical_position()) == "dangerous":
            hit_chance = random.random()
            if hit_chance < self.street.probability_of_hit_on_danger_zone:
                return True  # Collision occurs
        return False  # No collision
    
    def reached_sidewalk(self):
        '''
        Did we reach either the sidewalk we began crawling from or the other
        side? If so, the drunk survived.
        '''
        if self.drunk.get_vertical_position() > self.street.get_street_size() or self.drunk.get_vertical_position() < 0:
            return True
        return False
    
    def finished_game(self):
        '''
        Checks if any of the above cases were covered, compactly
        '''
        if self.check_collision():
            return "crash"
        elif self.reached_sidewalk():
            return "success"
        
class Scenario:
    def __init__(self, attempts, task):
        self.task = task
        self.street = Street()
        self.attempts = attempts
        self.seed = 43 # A seed for reproducability.
        self.walks = []
        
        random.seed(self.seed)
        
    def run_single_game(self):
        # Create a new drunk player every "single_game" to reinitialize him to position (0, 0)
        self.drunk = Drunk(task=self.task)
        # Create a grid in which the player interacts with the street and its danger zone
        self.grid = Grid(self.drunk, self.street)
        #initialize and take walk
        walk = []
        while True:
            walk.append(self.drunk.position) # save position
            self.drunk.move()
            reason = self.grid.finished_game()
            if reason:
                break
        self.walks.append(walk)
        return reason
    
    def run_games(self):
        '''
        Runs the function run_single_game, self.attempts times
        '''
        reasons = [] # Reasons why the game was aborted ("success"/"crash")
        for attempt in range(self.attempts):
            reasons.append(self.run_single_game())
        return reasons
            
    def return_walks(self):
        '''
        Return walks function for convenience.
        '''
        return self.walks

class Visualize:
    '''
    Implement a Visualize class here to visualize movements and results
    '''
    def __init__(self):
        pass

if __name__ == "__main__":  
    
    # Prepare scenario
    scenario = Scenario(attempts=2, task="A")
    
    # Run run_games
    print(scenario.run_games()) # Prints a list of the "success"/"crash" outcomes
    
    # Print walks
    print(scenario.return_walks()) # Prints the coordinates of the drunk man at each time step t; potentially useful for visualization, too.
