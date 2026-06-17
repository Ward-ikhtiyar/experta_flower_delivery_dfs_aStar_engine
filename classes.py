from experta import Fact, Field
from enums import FlowerColors
class Grid(Fact):
    max_x = Field(int, mandatory=True)
    max_y = Field(int, mandatory=True)

class Warehouse(Fact):
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)

class Pavilion(Fact):
    id = Field(int, mandatory=True)
    flower_type = Field(str, mandatory=True) 
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)
    demands_flowers=Field(bool,default=True)

class Robot(Fact):
    x=Field(int,mandatory=True)
    y=Field(int,mandatory=True)
    max_load=Field(int,default=0)
    is_filled=Field(bool,default=False)

class PavDemand(Fact):
    pav_id=Field(int,mandatory=True)
    # color=Field(str,mandatory=True)
    quantity=Field(int,mandatory=True)    
    processed=Field(bool,default=False)
  
