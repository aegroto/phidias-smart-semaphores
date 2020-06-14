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
from modules.roadpoint import RoadPoint, TargetRoadPoint

# start the actors
RoadPoint("A", "Sem1").start()
Semaphore("Sem1", "Sem2").start()
Semaphore("Sem2", "B").start()
TargetRoadPoint("B").start()

main().start()

# run the engine shell
PHIDIAS.shell(globals())