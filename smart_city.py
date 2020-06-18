import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

from modules.main import main
from modules.semaphore import Semaphore
from modules.roadpoint import RoadPoint, GoalRoadPoint

# start the actors
RoadPoint("A", "Sem1").start()
Semaphore("Sem1", "Sem2").start()
Semaphore("Sem2", "B").start()
GoalRoadPoint("B").start()

PHIDIAS.assert_belief(roadpoint("A"))
PHIDIAS.assert_belief(roadpoint("Sem1"))
PHIDIAS.assert_belief(roadpoint("Sem2"))
PHIDIAS.assert_belief(roadpoint("B"))

PHIDIAS.assert_belief(sem("Sem1"))
PHIDIAS.assert_belief(sem("Sem2"))

main().start()

# PHIDIAS.assert_belief(active("main"))
# PHIDIAS.assert_belief(congestion("Sem1"))
# PHIDIAS.assert_belief(congestion("Sem2"))

# run the engine shell
PHIDIAS.shell(globals())
