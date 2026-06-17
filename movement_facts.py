from experta import Fact,Field
from helper_facts import *

class FocusedNode(Fact):
    f_cost = Field(int, mandatory=True)
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)


class FrontierNode(Fact):
    cost=Field(int)
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)
    g = Field(int, mandatory=True)
    h = Field(int, mandatory=True)
    f = Field(int, mandatory=True)
    path_history = Field(tuple, default=())   
