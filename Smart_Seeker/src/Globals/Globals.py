# Global Vars
count = 0.1
direction = "right"


# Global Methods
class Globals:
    def __init__(this):
        #set global failTrigger variable for avoiding objects protocols
        this.failTrigger = False
        #set global variable for how far robot has progressed forward since last failTrigger
        this.timeForward = 0.0
        #set global lists for recording moves
        this.speedStack = []
        this.durationStack = []
        this.directionStack = []
        #set global variables for keeping track of search direction
        this.searchCount = 0.1
        this.searchDirection = "right"

    def set_failTrigger(this, state):
        this.failTrigger = state
    
    def update_timeForward(this, value):
        this.timeForward = this.timeForward + value
        
    def reset_timeForward(this):
        this.timeForward = 0
        
    def append_speedStack(this, value):
        this.speedStack.append(value)
    
    def append_durationStack(this, value):
        this.durationStack.append(value)
    
    def append_directionStack(this, value):
        this.directionStack.append(value)
        
    def pop_speedStack(this):
        this.speedStack.pop()
    
    def pop_durationStack(this):
        this.durationStack.pop()
    
    def pop_directionStack(this):
        this.directionStack.pop()

# Make instance
GlobalStacks = Globals()