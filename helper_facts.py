from experta import *
from enums import SearchAlgo
class InitializationComplete(Fact):
    pass

class PavTotalDemand(Fact):
    pav_id=Field(int,mandatory=True)
    quantity=Field(int,mandatory=True)
    processed=Field(bool,default=False)

class CurrentPav(Fact):
    pav_id=Field(int,mandatory=True)
    processed=Field(bool,default=False)

class RobotGoWareHouse(Fact):
    pass    

class CheckRobot(Fact):
    pass   

class Visited(Fact):
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)

class TargetNode(Fact):
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)

class SearchNode(Fact):
    cost=Field(int)
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)
    path_history = Field(tuple, default=())   
    processed=Field(bool,default=False) 

class AStarSearchNode(Fact):
    cost=Field(int)
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)
    g = Field(int, mandatory=True)
    h = Field(int, mandatory=True)
    f = Field(int, mandatory=True)
    path_history = Field(tuple, default=())   
    processed=Field(bool,default=False)     

class TrackBackNode(Fact):
    path_history = Field(tuple, default=())    
    

class RobotReachedTarget(Fact):
    pass

class CleanupSearchNodes(Fact):
     
    pass

class CleanupFrontierNodes(Fact):
     
    pass

class SearchMethod(Fact):
    method=Field(SearchAlgo,default=SearchAlgo.DFS)

class MakeAMove(Fact):
    pass    

class StepCounter(Fact):
    count=Field(int,default=0)

class CountSteps(Fact):
    path_history = Field(tuple, default=())   
    