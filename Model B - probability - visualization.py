import random
import numpy as np #added by Deveney hehe!
import matplotlib.pyplot as plt #added by Deveney hehe

class Drunk:
    '''
    This represents a drunk person who includes an own time measure, a distance
    measure, and may be made to behave differently depending on the task.
    '''
    def __init__(self, task): #__init__(self) : This is the constructor method in Python, which is called when an instance of the class is created.
        self.time = 0  # Start time
        self.velocity = 2 # Walk speed
        self.task = task
        if task == "A":
            self.position = (0, 0)
        elif self.task == "B" or self.task == "C":
            self.old_direction = 0 #Heading direction - added by Deveney
            self.position = (0., 0.) # Float point values for tasks B and C
        else: 
            ValueError("Invalid Task")

    def move(self):
        if self.task == "A":
            rand_value = random.random() #that generates a random floating-point number between 0.0 (inclusive) and 1.0 (exclusive).
            if rand_value < 0.25:
                self.position = (self.position[0] - self.velocity, self.position[1]) # Move left; 如果if 沒滿足，則往elif跑，代表已知value為>= 0.25
            elif rand_value < 0.5:
                self.position = (self.position[0] + self.velocity, self.position[1]) # Move right; [0]為左右 [1]為上下
            else:
                self.position = (self.position[0], self.position[1] + self.velocity) # Move straight
            
            
        elif self.task == "B":  # case B - added by Deveney
                                # the direction of the first step is randomly picked, which means that the game will end immediately once the angle is minus.
            angle = np.linspace(-2/3 * np.pi, 2/3 *np.pi, 240) #randomly pick the turning angle in radians
            self.new_direction = random.choice(angle)
            self.old_direction += self.new_direction #accumulate the turning angle to compute the movement in x-y coordinate system.
            self.position = (self.position[0] + float(np.cos(self.old_direction))*self.velocity , self.position[1] + float(np.sin(self.old_direction))*self.velocity)
            
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
    def __init__(self): #initializes the object's attributes / Automatically called when you create an object of the class.
                        #Always take self as the first parameter to refer to the instance itself.
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
                return zone.zone_type  #but how to distinguish? I didn't see the relative values
            current_position += zone.length    #如果position 不在第一個zone type，則跳到第二個zone ye 進行判別
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
            hit_chance = random.random() #generate a value between [0, 1)
            if hit_chance < self.street.probability_of_hit_on_danger_zone:
                return True  # Collision occurs
        return False  # No collision
    
    def reached_sidewalk(self):
        '''
        Did we reach either the sidewalk we began crawling from or the other
        side? If so, the drunk survived.
        '''
        if self.drunk.get_vertical_position() >= self.street.get_street_size() or self.drunk.get_vertical_position() < 0:
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
        random.seed(self.seed) #這到底是甚麼
        
    def run_single_game(self):
        self.drunk = Drunk(task=self.task) # Create a new drunk player every "single_game" to reinitialize him to position (0, 0)
        self.grid = Grid(self.drunk, self.street) # Create a grid in which the player interacts with the street and its danger zone
        walk = [] #initialize and take walk
        walk.append(self.drunk.position)
        while True:
            self.drunk.move()
            walk.append(self.drunk.position) # save position
            reason = self.grid.finished_game()
            if reason:
                break
        self.walks.append(walk)
        
        return reason
    
    def run_games(self):
        '''
        Runs the function run_single_game, self.attempts times
        '''
        reasons = []    # Reasons why the game was aborted ("success"/"crash")
                        # The empty list reasons = [] is initialized as a container to store the outcomes of each game run by the run_games() method in your program.
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
            

    def plot_the_walk(self,position):
        plt.ion() #turn on interactive mode
        self.fig, self.ax = plt.subplots()  # Create figure and axis
        self.ax.set_xlim(-10, 10) 
        self.ax.set_ylim(-2, 8)
        # Plot the background highlights
        highlight_regions = [(1, 3), (5, 7)]
        for start, end in highlight_regions:
            self.ax.axhspan(start, end, color='red', alpha=0.3)

        self.line, = self.ax.plot([], [], marker='o')  # Initialize the line for plotting

        x=[(t[0]) for t in position[0]] # Extract all the first values from the tuples
        y=[(t[1]) for t in position[0]] # Extract all the second values from the tuples
        print(x)
        print('-----')
        print(y)
        self.line.set_xdata(x)
        self.line.set_ydata(y)
        self.ax.relim()  # Recalculate limits
        self.ax.autoscale_view()  # Rescale plot view
        plt.draw()
        plt.pause(1)  # Pause to create animation effect
        plt.show()  # Show the final plot

    def plot_survival_rate(self,survival_values,project_list):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], marker='o', linestyle='-', color='b')  # Initialize line for plotting
        x = project_list
        y = survival_values
        print(f"method x: {x}")
        print(f"survival rate y: {y}")
        self.ax.bar(x, y, color='blue', alpha=0.7)
        self.ax.set_xlabel('Projects')
        self.ax.set_ylabel('Survival Probability (%)')
        self.ax.set_title('Survival Probability for Each Method')
        self.ax.set_xticks(x)  # Set positions of the x-ticks to the project names
        self.ax.set_xticklabels(x)  # Set the x-tick labels to the project names
        plt.show()
        

 

class probability_computing:
    '''
    to compute the survival probability
    '''
    def __init__(self, result):
        self.results = result
        self.number_of_sc = [0, 0]
        self.survival = 0

    def calculating(self):
        self.number_of_sc = [self.results.count("success"),self.results.count("crash")]
        if len(self.results) > 0: 
            self.survival = self.number_of_sc[0]/ len(self.results) *100
        else:
            self.survival =0
        return self.survival
                       
    def print_results(self):
        self.calculating()
        print(f"Success count: {self.number_of_sc[0]}")
        print(f"Crash count: {self.number_of_sc[1]}")
        print(f"probability of survival: {self.survival}%")
        

if __name__ == "__main__":  #If the script is run directly (e.g., python script.py), the value of __name__ is set to "__main__".

    project_list= ["A", "B"]
    survival_values= []
    
    i= 0
    while i < len(project_list) :
        scenario = Scenario(attempts=10, task=project_list[i])   # Prepare scenario
        result= scenario.run_games()                            # Run run_games
        print(f"Results for project {project_list[i]}: {result}")                                           # Prints a list of the "success"/"crash" outcomes        
        probability = probability_computing(result)             # Run probability_computing
        survival = probability.calculating()
        probability.print_results()
        survival_values.append(survival)      
        i += 1
        vis = Visualize()
        position = scenario.return_walks()
        
        print(f"position: {position}")
        vis.plot_the_walk(position) # plot how they walk at their first attemp
        
        
    vis.plot_survival_rate(survival_values, project_list) #plot the survival rate
    
    # Print walks
    # print(scenario.return_walks()) # Prints the coordinates of the drunk man at each time step t; potentially useful for visualization, too.

