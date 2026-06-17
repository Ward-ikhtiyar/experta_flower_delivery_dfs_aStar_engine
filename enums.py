from enum import Enum

class SearchAlgo(Enum):
    DFS = "DFS"
    ASTAR = "A*"

class FlowerColors(Enum):
    BROWN = "بني"
    PINK = "وردي"
    LIGHT_PINK = "فاتح"
    YELLOW = "أصفر"
    RED = "أحمر"
    WHITE = "أبيض"
    GREEN = "أخضر"
    CORAL = "مرجاني"
    PURPLE = "أرجواني"


class Flower(Enum):
    ROSE = "جوري"
    TULIP = "توليب"
    ORCHID = "أوركيد"  
    GOLIAT_ROSE ="جاين جولييت"

    