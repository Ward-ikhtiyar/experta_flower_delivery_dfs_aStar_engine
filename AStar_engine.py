
from experta import *
from classes import *
from helper_facts import *
from movement_facts import *
from enums import SearchAlgo
import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

class AStarFlowerDeliveryEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        print("Engine initialized and ready!")
    
    @Rule(NOT(PavTotalDemand(processed=False)))
    def finish_initalization(self):
        self.declare(InitializationComplete())

    @Rule(Pavilion(id=MATCH.id, demands_flowers=True),
          NOT(CurrentPav()),
          InitializationComplete())
    def set_current_focused(self, id):
        self.declare(CurrentPav(pav_id=id))
        print(f"[Rule Fired] We set a current pav with id {id}")

    @Rule(CurrentPav(pav_id=MATCH.pav_id, processed=False), Robot(is_filled=False))
    def instruct_robot_to_fill(self, pav_id):
        self.declare(RobotGoWareHouse())    
        print(f"[Rule Fired] Robot is going to load the order for Pav: {pav_id}")

    @Rule(Warehouse(x=MATCH.x, y=MATCH.y),
          NOT(TargetNode()),
          Robot(x=MATCH.rx, y=MATCH.ry),
          AS.rgwh << RobotGoWareHouse())
    def robot_go_warehouse_initial(self, rgwh, x, y, rx, ry):
        self.retract(rgwh)
        self.declare(TargetNode(x=x, y=y))
        h = abs(x - rx) + abs(y - ry)
        self.declare(AStarSearchNode(x=rx, y=ry, path_history=((rx, ry),), g=0, h=h, f=h, processed=False))
        print(f"[Rule Fired] robot_go_warehouse_initial")

    @Rule(
          AStarSearchNode(x=MATCH.x, y=MATCH.y, f=MATCH.s_cost, processed=False),
          NOT(FocusedNode()),
          salience=20
          )    
    def assign_inital_focused(self, x, y, s_cost):
        self.declare(FocusedNode(f_cost=s_cost, x=x, y=y))
        print(f"[A* Queue] Initial focus set to node ({x}, {y}) with f={s_cost}")
    
    @Rule(
          AStarSearchNode(x=MATCH.x, y=MATCH.y, f=MATCH.s_cost, processed=False),
          AS.focusNode << FocusedNode(f_cost=MATCH.f_cost),
          TEST(lambda s_cost, f_cost: s_cost < f_cost),
          salience=30
          )  
    def update_focused(self, focusNode, s_cost, x, y):
        self.modify(focusNode, f_cost=s_cost, x=x, y=y) 
        print(f"[A* Queue] Focus updated to better node ({x}, {y}) with f={s_cost}")
    @Rule(
        
        AS.focus << FocusedNode(x=MATCH.tx, y=MATCH.ty),
        AStarSearchNode(x=MATCH.tx, y=MATCH.ty, path_history=MATCH.history,f=MATCH.f),
        AS.target << TargetNode(x=MATCH.tx, y=MATCH.ty),
        AS.robot << Robot(),
        salience=10
    )
    def target_has_reached_ASTAR(self, focus, target, tx, ty, robot, history,f):
        self.retract(focus)
        self.retract(target) 
        self.modify(robot, x=tx, y=ty)
        self.declare(RobotReachedTarget())
        self.declare(CleanupFrontierNodes())
        print(f"""\n[Rule Fired] Robot reached its target via path: {history}\n with cost: {f}""")

    @Rule(
        
        FocusedNode(x=MATCH.cx, y=MATCH.cy),
        AStarSearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history, g=MATCH.g, processed=False),
        TargetNode(x=MATCH.tx, y=MATCH.ty),
        Grid(max_x=MATCH.x_bounds, max_y=MATCH.y_bounds),
        TEST(lambda y_bounds, cy: cy + 1 <= y_bounds),
        TEST(lambda cx, cy, history: (cx, cy + 1) not in history)
    )
    def branch_right_astar(self, cx, cy, history, g, tx, ty):
        new_x, new_y = cx, cy + 1
        new_g = g + 1
        h = abs(tx - new_x) + abs(ty - new_y)
        f = new_g + h
        self.declare(AStarSearchNode(
            x=new_x, y=new_y, path_history=history + ((new_x, new_y),), g=new_g, h=h, f=f, processed=False
        ))
        print(f"[A*] RIGHT → ({new_x}, {new_y}) | f={f}")

    @Rule(
        
        FocusedNode(x=MATCH.cx, y=MATCH.cy),
        AStarSearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history, g=MATCH.g, processed=False),
        TargetNode(x=MATCH.tx, y=MATCH.ty),
        Grid(max_x=MATCH.x_bounds, max_y=MATCH.y_bounds),
        TEST(lambda cy: cy - 1 >= 1),
        TEST(lambda cx, cy, history: (cx, cy - 1) not in history)
    )
    def branch_left_astar(self, cx, cy, history, g, tx, ty):
        new_x, new_y = cx, cy - 1
        new_g = g + 1
        h = abs(tx - new_x) + abs(ty - new_y)
        f = new_g + h
        self.declare(AStarSearchNode(
            x=new_x, y=new_y, path_history=history + ((new_x, new_y),), g=new_g, h=h, f=f, processed=False
        ))
        print(f"[A*] LEFT → ({new_x}, {new_y}) | f={f}")

    @Rule(
        
        FocusedNode(x=MATCH.cx, y=MATCH.cy),
        AStarSearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history, g=MATCH.g, processed=False),
        TargetNode(x=MATCH.tx, y=MATCH.ty),
        Grid(max_x=MATCH.x_bounds, max_y=MATCH.y_bounds),
        TEST(lambda x_bounds, cx: cx + 1 <= x_bounds),
        TEST(lambda cx, cy, history: (cx + 1, cy) not in history)
    )
    def branch_down_astar(self, cx, cy, history, g, tx, ty):
        new_x, new_y = cx + 1, cy
        new_g = g + 1
        h = abs(tx - new_x) + abs(ty - new_y)
        f = new_g + h
        self.declare(AStarSearchNode(
            x=new_x, y=new_y, path_history=history + ((new_x, new_y),), g=new_g, h=h, f=f, processed=False
        ))
        print(f"[A*] DOWN → ({new_x}, {new_y}) | f={f}")

    @Rule(
        
        FocusedNode(x=MATCH.cx, y=MATCH.cy),
        AStarSearchNode(x=MATCH.cx, y=MATCH.cy, path_history=MATCH.history, g=MATCH.g, processed=False),
        TargetNode(x=MATCH.tx, y=MATCH.ty),
        Grid(max_x=MATCH.x_bounds, max_y=MATCH.y_bounds),
        TEST(lambda cx: cx - 1 >= 1),
        TEST(lambda cx, cy, history: (cx - 1, cy) not in history)
    )
    def branch_up_astar(self, cx, cy, history, g, tx, ty):
        new_x, new_y = cx - 1, cy
        new_g = g + 1
        h = abs(tx - new_x) + abs(ty - new_y)
        f = new_g + h
        self.declare(AStarSearchNode(
            x=new_x, y=new_y, path_history=history + ((new_x, new_y),), g=new_g, h=h, f=f, processed=False
        ))
        print(f"[A*] UP → ({new_x}, {new_y}) | f={f}")

    @Rule(
        
        AS.focus << FocusedNode(x=MATCH.cx, y=MATCH.cy),
        AS.current_node << AStarSearchNode(x=MATCH.cx, y=MATCH.cy, processed=False),
        salience=-10  
        )
    def close_node_expansion(self, focus, current_node):
        self.modify(current_node, processed=True)
        self.retract(focus)
        print(f"[A* Queue] Closed node ({current_node['x']}, {current_node['y']})")

    @Rule(CleanupFrontierNodes(), AS.stray_node << AStarSearchNode())
    def delete_leftover_search_nodes(self, stray_node):
        self.retract(stray_node)

    @Rule(AS.cleanup << CleanupFrontierNodes(), NOT(AStarSearchNode()))
    def finish_node_cleanup(self, cleanup):
        self.retract(cleanup)
        print(f"[Rule Fired] Cleaned up memory from search nodes")

    @Rule(AS.rrt << RobotReachedTarget(),
          AS.robot << Robot(is_filled=False))
    def load_robot(self, robot, rrt):
        self.modify(robot, is_filled=True)
        self.retract(rrt)
        print(f"[Rule Fired] Robot loaded from warehouse")

    @Rule(AS.rrt << RobotReachedTarget(),
          AS.robot << Robot(is_filled=True),
          AS.current_pav << CurrentPav(pav_id=MATCH.pav_id),
          AS.pav << Pavilion(id=MATCH.pav_id))
    def unload_robot(self, robot, rrt, current_pav, pav_id, pav):
        self.modify(robot, is_filled=False)
        self.retract(rrt)
        self.retract(current_pav)
        self.modify(pav, demands_flowers=False)
        print(f"[Rule Fired] Robot unloaded into pavilion {pav_id}")    

    @Rule(NOT(Pavilion(demands_flowers=True)), NOT(CurrentPav()))
    def congrats_user(self):
        print(f"\n[Congrats!] All pavilions have been successfully filled!")    

    @Rule(
          CurrentPav(pav_id=MATCH.current_id),
          Robot(x=MATCH.current_x, y=MATCH.current_y, is_filled=True),
          Pavilion(id=MATCH.current_id, x=MATCH.pav_x, y=MATCH.pav_y, demands_flowers=True))
    def go_to_unload_in_pav(self, current_id, current_x, current_y, pav_x, pav_y):
        print(f"[Rule Fired] Robot is moving to unload his load in pav {current_id}")
        self.declare(TargetNode(x=pav_x, y=pav_y))
        
        h = abs(pav_x - current_x) + abs(pav_y - current_y)
        self.declare(AStarSearchNode(x=current_x, y=current_y, path_history=((current_x, current_y),), g=0, h=h, f=h, processed=False))