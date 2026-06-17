from experta import *
from classes import *
from helper_facts import *
from movement_facts import *
from enums import SearchAlgo
import collections
import collections.abc

collections.Mapping = collections.abc.Mapping
class FlowerDeliveryEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        print("ward is here")

    #////////////////////////////////////////////////////////////////    
    # @Rule(
    #     AS.demand << PavDemand(pav_id=MATCH.id, quantity=MATCH.qty, processed=False),
    #     NOT(PavTotalDemand(pav_id=MATCH.id)),
    #     salience=120
    # )
    # def create_total(self, demand, id, qty):
    #     self.declare(PavTotalDemand(pav_id=id, quantity=qty))
    #     self.modify(demand, processed=True)
    #     print(f"[Rule Fired] create_total")

    # @Rule(
    #     AS.demand << PavDemand(pav_id=MATCH.id, quantity=MATCH.qty, processed=False),
    #     AS.total << PavTotalDemand(pav_id=MATCH.id, quantity=MATCH.total_qty),
    #     salience=100
    # )
    # def update_total(self, demand, total, qty, total_qty):
    #     self.modify(total, quantity=total_qty + qty, processed=False)
    #     self.modify(demand, processed=True)
    #     print(f"[Rule Fired] update_total")
    
    # @Rule(
    #     AS.robot << Robot(max_load=MATCH.current),
    #     AS.totDemand << PavTotalDemand(quantity=MATCH.q),
    #     TEST(lambda current, q: q > current),
    #     NOT(PavDemand(processed=False)), 
    #     salience=10
    # )
    # def update_max_load(self, robot,totDemand, q):
    #     self.modify(robot, max_load=q)
    #     self.modify(totDemand,processed=True)
    #     print(f"[Rule Fired] Bumping robot max_load capacity to: {q}")
        
    #////////////////////////////////////////////////////////////////    
    @Rule(NOT(PavTotalDemand(processed=False)))
    def finish_initalization(self):
        self.declare(InitializationComplete())
        
    #////////////////////////////////////////////////////////////////    
    @Rule(Pavilion(id=MATCH.id,demands_flowers=True),
        NOT(CurrentPav()),
        InitializationComplete(),)
    def set_current_focused(self,id):
        self.declare(CurrentPav(pav_id=id))
        print(f"[Rule Fired] we set a current pav with id {id}")

    @Rule(CurrentPav(pav_id=MATCH.pav_id,processed=False),Robot(is_filled=False))
    def instruct_robot_to_fill(self,pav_id):
        self.declare(RobotGoWareHouse())    
        print(f"[Rule Fired] Robot is Goin for loading the order of Pav : {pav_id}")
    
    @Rule(Warehouse(x=MATCH.x,y=MATCH.y),
          NOT(TargetNode()),
          Robot(x=MATCH.rx,y=MATCH.ry),
          AS.rgwh << RobotGoWareHouse())
    def robot_go_warehouse_initial(self,rgwh,x,y,rx,ry):
        self.retract(rgwh)
        self.declare(TargetNode(x=x,y=y))
        self.declare(SearchNode(x=rx,y=ry,path_history=((rx, ry),),))
        print(f"[Rule Fired] robot_go_warehouse_initial")
    @Rule(
        AS.search << SearchNode(x=MATCH.tx, y=MATCH.ty,path_history=MATCH.history),
        AS.target << TargetNode(x=MATCH.tx, y=MATCH.ty),
        AS.robot << Robot(),
        salience=100
    )
    def target_has_reached(self, search, target,tx,ty,robot,history):
        self.retract(search)
        self.retract(target) 
        self.modify(robot,x=tx,y=ty)
        self.declare(RobotReachedTarget())
        self.declare(CleanupSearchNodes())
        print(f"[Rule Fired] robo reached his target")

    @Rule(
        CleanupSearchNodes(),
        AS.stray_node << SearchNode()
    )
    def delete_leftover_search_nodes(self, stray_node):
        self.retract(stray_node)

    @Rule(
        AS.cleanup << CleanupSearchNodes(),
        NOT(SearchNode())
    )
    def finish_node_cleanup(self, cleanup):
        self.retract(cleanup)
        print(f"[Rule Fired] cleaned up memory from search nodes ")


    @Rule(AS.rrt << RobotReachedTarget(),
          AS.robot << Robot(is_filled=False))
    def load_robot(self,robot,rrt):
        self.modify(robot,is_filled=True)
        self.retract(rrt)
        self.declare(MakeAMove())
        print(f"[Rule Fired] robot load from ware house")

    @Rule(AS.rrt << RobotReachedTarget(),
          AS.robot << Robot(is_filled=True),
          AS.current_pav << CurrentPav(pav_id=MATCH.pav_id),
          AS.pav << Pavilion(id=MATCH.pav_id)
          )
    def unload_robot(self,robot,rrt,current_pav,pav_id,pav):
        self.modify(robot,is_filled=False)
        self.retract(rrt)
        self.retract(current_pav)
        self.modify(pav,demands_flowers=False)
        self.declare(MakeAMove())
        print(f"[Rule Fired] robo unloaded into pavilion {pav_id}")    

    @Rule(NOT(Pavilion(demands_flowers=True)),NOT(CurrentPav()),StepCounter(count=MATCH.count))
    def congrats_user(self,count):
        print(f"[Congrats!] all pavilions has been filled")
        print(f"[Analysis] step count:{count}  ")

        

#????????????????????????????? MOVEMENT RULES ?????????????????????????????????????????????? 
    @Rule(
        AS.current_node << SearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history),
        Grid(max_y=MATCH.y_bounds),
        TEST(lambda y_bounds, cy: cy + 1 <= y_bounds),
        TEST(lambda cx, cy, history: (cx, cy + 1) not in history)
    )
    def branch_right(self, cx, cy, history):
        new_y = cy + 1
        new_history = history + ((cx, cy),)
        self.declare(SearchNode(x=cx, y=new_y, path_history=new_history))
        self.declare(MakeAMove())
        print(f"[DFS Branch] Expanded RIGHT to ({cx}, {new_y})")
    @Rule(
        AS.current_node << SearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history),
        TEST(lambda cy: cy - 1 >= 1),
        TEST(lambda cx, cy, history: (cx, cy - 1 ) not in history)
    )
    def branch_left(self, cx, cy, history):
        new_y = cy - 1
        new_history = history + ((cx, cy),)
        self.declare(SearchNode(x=cx, y=new_y, path_history=new_history))
        self.declare(MakeAMove())
        print(f"[DFS Branch] Expanded LEFT to ({cx}, {new_y})")
    @Rule(
        AS.current_node << SearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history),
        Grid(max_x=MATCH.x_bounds),
        TEST(lambda x_bounds, cx: cx + 1 <= x_bounds),
        TEST(lambda cx, cy, history: (cx + 1, cy) not in history)
    )
    def branch_down(self, cx, cy, history):
        new_x = cx + 1
        new_history = history + ((cx, cy),)
        self.declare(SearchNode(x=new_x, y=cy, path_history=new_history))
        self.declare(MakeAMove())
        print(f"[DFS Branch] Expanded DOWN to ({new_x}, {cy})")
    @Rule(
        AS.current_node << SearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history),
        TEST(lambda cx: cx - 1 >= 1),
        TEST(lambda cx, cy, history: (cx - 1, cy) not in history)
    )
    def branch_up(self, cx, cy, history):
        new_x = cx - 1
        new_history = history + ((cx, cy),)
        self.declare(SearchNode(x=new_x, y=cy, path_history=new_history))
        self.declare(MakeAMove())
        print(f"[DFS Branch] Expanded UP to ({new_x}, {cy})")

#????????????????????????????? MOVEMENT RULES END ??????????????????????????????????????????????     
    @Rule(CheckRobot(),
          Robot(x=MATCH.x,y=MATCH.y)
          )
    def check_robot_axis(self,x,y):
        print(f"[Rule Fired] robot is at position {x} {y} ")
    
    @Rule(
          CurrentPav(pav_id=MATCH.current_id),
          Robot(x=MATCH.current_x,y=MATCH.current_y,is_filled=True),
          Pavilion(id=MATCH.current_id,x=MATCH.pav_x,y=MATCH.pav_y,demands_flowers=True))
    def go_to_unload_in_pav(self,current_id,current_x,current_y,pav_x,pav_y):
        print(f"[Rule Fired] robot is unlloading hsi load in pav {current_id}")
        self.declare(TargetNode(x=pav_x, y=pav_y))
        self.declare(SearchNode(x=current_x,y=current_y,path_history=((current_x,current_y))))
        
    
    @Rule(AS.move << MakeAMove(),AS.stepCounter << StepCounter(count=MATCH.count),salience=150)
    def update_counter(self,stepCounter,count,move):
        new_count=count+1
        self.modify(stepCounter,count=new_count)
        self.retract(move)




        
       
         