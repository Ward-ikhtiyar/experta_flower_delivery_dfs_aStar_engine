import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from classes import *
from helper_facts import *
from engine import *
from AStar_engine import *

from movement_facts import *



# myengine = FlowerDeliveryEngine()
myengine = AStarFlowerDeliveryEngine() # ASTAR ENGINE 

myengine.reset()


myengine.declare(
    Grid(max_x=5,max_y=5))

myengine.declare(Warehouse(x=2,y=3))

myengine.declare(Robot(x=1,y=3,max_load=4))

myengine.declare(
    Pavilion(
        id=1,
        flower_type="Rose",
        x=4,
        y=2,
        demands_flowers=True)
)

myengine.declare(
    Pavilion(
        id=2,
        flower_type="Tulip",
        x=3,
        y=4,
        demands_flowers=True)
)

myengine.declare(
    Pavilion(
        id=3,
        flower_type="Orchid",
        x=5,
        y=4,
        demands_flowers=True)
)

myengine.declare(
    Pavilion(
        id=4,
        flower_type="Juliet Rose",
        x=2,
        y=5,
        demands_flowers=True)
)

myengine.declare(PavDemand(pav_id=1,   quantity=2, processed=False))
myengine.declare(PavDemand(pav_id=1,  quantity=1, processed=False))
myengine.declare(PavDemand(pav_id=1, quantity=1, processed=False))

myengine.declare(PavDemand(pav_id=2,   quantity=3, processed=False))
myengine.declare(PavDemand(pav_id=2,quantity=1, processed=False))

myengine.declare(PavDemand(pav_id=3,quantity=2, processed=False))
myengine.declare(PavDemand(pav_id=3,  quantity=1, processed=False))

myengine.declare(PavDemand(pav_id=4,  quantity=2, processed=False))
myengine.declare(PavDemand(pav_id=4,  quantity=2, processed=False))

myengine.declare(InitializationComplete())
myengine.declare(StepCounter())

myengine.run()

